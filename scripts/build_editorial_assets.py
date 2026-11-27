"""Build the recommendation cards, rating badges and comparison graphics.

Run with Python 3.9+: python scripts/build_editorial_assets.py
Uses only the standard library. Existing cover illustrations stay hand-authored.
"""
from html import escape
from math import cos, sin, pi
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
SERIF = "Georgia,'Noto Serif CJK SC','Songti SC',SimSun,serif"
SANS = "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif"
MONO = "Consolas,'Liberation Mono',monospace"
GOLD = '#edc17e'
CREAM = '#fff4d6'


def text(x, y, value, size, fill=CREAM, font=SANS, weight=400, extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{escape(value)}</text>')


def rect(x, y, w, h, fill, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


def line(x, y, x2, y2, color=GOLD, extra=''):
    return f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{color}" {extra}/>'


def star(x, y, r, filled=True):
    points = []
    for i in range(10):
        a = -pi / 2 + i * pi / 5
        radius = r if i % 2 == 0 else r * .44
        points.append(f'{x + cos(a) * radius:.2f},{y + sin(a) * radius:.2f}')
    return (f'<polygon points="{" ".join(points)}" fill="{GOLD if filled else "none"}" '
            f'stroke="{GOLD}" stroke-width="1.5" stroke-linejoin="round"/>')


def stars(x, y, rating, r=12, gap=32):
    return ''.join(star(x + i * gap, y, r, i < rating) for i in range(5))


def save(name, w, h, title, description, body):
    document = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">\n'
                f'<title id="title">{escape(title)}</title>\n'
                f'<desc id="desc">{escape(description)}</desc>\n{body}\n</svg>\n')
    (ASSETS / name).write_text(document, encoding='utf-8')


def medallion(x, y, kind):
    body = '<circle r="49" fill="none" stroke="#edc17e"/><circle r="43" fill="none" stroke="#edc17e" opacity=".4"/>'
    if kind == 'niva':
        body += ('<circle r="27" fill="none" stroke="#9adcc8" stroke-width="2"/>'
                 '<ellipse rx="12" ry="27" fill="none" stroke="#9adcc8" stroke-width="2"/>'
                 '<path d="M-27 0h54m-50-13h46m-46 26h46" stroke="#9adcc8" fill="none"/>'
                 '<path d="M-36 22Q-4-35 34-16" stroke="#edc17e" stroke-width="3" fill="none"/>'
                 '<circle cx="31" cy="-17" r="4" fill="#edc17e"/>')
    else:
        body += ('<path d="M-29 0L0-25 29 0M-22-5v31h44V-5" fill="none" stroke="#edc17e" stroke-width="3" stroke-linejoin="round"/>'
                 '<path d="M-13 5h11v10h-11Z" fill="#ffa598"/>'
                 '<path d="M7 5h9v21H7Z" fill="#9adcc8"/>'
                 '<path d="M-33 32h66" stroke="#edc17e"/>')
    return f'<g transform="translate({x} {y})">{body}</g>'


def featured_card(x, y, w, kind):
    niva = kind == 'niva'
    bg = '#223f47' if niva else '#39304e'
    accent = '#9adcc8' if niva else '#ecc0d3'
    name = 'NIVA Network' if niva else '苏菲家宽'
    title = '低预算，探索家宽' if niva else '按需求，挑住宅出口'
    subtitle = '多地区家宽体验 · 月付试用' if niva else '静态住宅 / 动态家宽 · 分档选择'
    body = rect(0, 0, w, 352, bg)
    body += rect(1, 1, w-2, 350, 'none', 'stroke="#ba9c6f"')
    body += rect(9, 9, w-18, 334, 'none', 'stroke="#ba9c6f" opacity=".35"')
    body += line(28, 65, w-28, 65, GOLD, 'opacity=".5"')
    body += text(28, 42, '01 / NIVA' if niva else '02 / SUFE', 18, GOLD, MONO, 700, 'letter-spacing="2"')
    body += text(w-28, 42, '特别推荐', 18, GOLD, SANS, 500, 'text-anchor="end"')
    body += text(27, 127, name, 44 if niva else 48, CREAM, SERIF, 700)
    body += text(29, 171, title, 27, accent, SANS, 700)
    body += text(29, 210, subtitle, 23, CREAM)
    body += stars(42, 264, 5, 14, 37)
    body += text(229, 272, '5 / 5', 24, GOLD, MONO, 700)
    body += text(29, 320, '主观推荐 · 基于现有资料', 20, '#e0d3bd')
    body += medallion(w-80, 278, kind)
    return f'<g transform="translate({x} {y})">{body}</g>'


def featured(mobile):
    w, h = (600, 796) if mobile else (1160, 420)
    body = rect(0, 0, w, h, '#1e263b')
    body += text(24, 35, 'THE RESIDENTIAL EDIT', 17, GOLD, MONO, 700, 'letter-spacing="2"')
    body += text(w-24, 35, '家宽精选', 18, CREAM, SANS, 600, 'text-anchor="end"')
    if mobile:
        body += featured_card(16, 56, 568, 'niva')
        body += featured_card(16, 428, 568, 'sufe')
    else:
        body += featured_card(16, 54, 554, 'niva')
        body += featured_card(590, 54, 554, 'sufe')
    save('featured-picks-mobile.svg' if mobile else 'featured-picks.svg', w, h,
         'NIVA Network × 苏菲家宽 · 家宽精选',
         '两家均为主观推荐五星。NIVA：低预算体验多地区家宽；苏菲：按需比较静态住宅与动态家宽。评分基于现有资料，不是实测排名。', body)


def rating_badges():
    for score in (3, 4, 5):
        body = rect(0, 0, 450, 64, '#262b4e', 'rx="6"')
        body += rect(.75, .75, 448.5, 62.5, 'none', 'rx="6" stroke="#b19568" stroke-width="1.5"')
        body += text(18, 40, '主观推荐', 20, CREAM, SANS, 600)
        body += line(116, 17, 116, 47, GOLD, 'opacity=".4"')
        body += stars(146, 32, score, 13, 34)
        body += text(350, 41, f'{score} / 5', 25, GOLD, MONO, 700)
        save(f'rating-{score}.svg', 450, 64, f'主观推荐 {score}/5',
             f'五颗星中点亮{score}颗。基于已有资料的选购判断，不代表统一实测或服务保证。', body)


def mobile_routes():
    routes = [
        ('daily', '01 / DAILY', '日常主力', '守候网络', '#253e69', '#ffa77b'),
        ('backup', '02 / BACKUP', '备用流量', '吹雪云', '#563e68', '#d5b5ef'),
        ('regions', '03 / REGIONS', '多地区', 'TAG', '#235955', '#9adcc8'),
        ('residential', '04 / HOME', '住宅家宽', '苏菲家宽', '#6b3b4d', '#ffbb9b'),
    ]
    for slug, label, title, provider, bg, accent in routes:
        body = rect(0, 0, 480, 280, bg)
        body += rect(0, 0, 480, 6, accent)
        body += rect(10, 16, 460, 254, 'none', f'stroke="{accent}" opacity=".45"')
        body += text(28, 55, label, 22, accent, MONO, 700, 'letter-spacing="1"')
        body += text(26, 138, title, 62, CREAM, SERIF, 700)
        body += line(28, 168, 452, 168, accent, 'opacity=".6"')
        body += text(28, 235, provider, 45, CREAM, SANS, 700)
        body += '<path d="M387 220h48m-13-13 13 13-13 13" fill="none" stroke="'+accent+'" stroke-width="4"/>'
        save(f'pick-{slug}-mobile.svg', 480, 280, f'{title}：{provider}', f'点击查看{provider}的套餐、评测与资料日期。', body)


def budget_cards():
    cards = [
        ('ai', 'AI 入门', 'FlyBit', '#391d54', '#ffb7df', '#9e5eae', '#613583',
         '<path d="M239 54h64v38h-28l-13 11V92h-23Z" fill="#ffb7df"/>'
         '<path d="M250 64h42v4h-42zm0 10h30v4h-30z" fill="#391d54"/>'
         '<path d="M288 38v19m-9-9h18" stroke="#fff1a8" stroke-width="3"/>'),
        ('daily', '日常主力', '守候网络', '#142f57', '#b6ebff', '#377da4', '#23517a',
         '<path d="M233 87a36 36 0 0 1 72 0" fill="#87d8ff"/>'
         '<path d="m222 96 24-26 15 14 12-10 30 22Z" fill="#205479"/>'
         '<path d="M229 97c23 0 38-13 72-15" fill="none" stroke="#ffe087" stroke-width="5"/>'
         '<circle cx="274" cy="87" r="5" fill="#fff1bd"/>'),
        ('backup', '低价备用', '吹雪云', '#4c2425', '#ffd3a3', '#ba5e43', '#823c35',
         '<path d="M241 56h60v44h-60z" fill="#ffcc78"/>'
         '<path d="M255 50h29v12h-29z" fill="#ffecae"/>'
         '<path d="m276 61-15 17h10l-4 15 17-20h-11z" fill="#6b3529"/>'
         '<path d="M230 66h7m-11 10h8m-4 10h7" stroke="#ffd3a3" stroke-width="3"/>'),
        ('home', '住宅出口', 'NIVA / 苏菲', '#103b34', '#b5f3ca', '#4b9783', '#286657',
         '<path d="m231 72 24-21 24 21v27h-48z" fill="#b5f3ca"/>'
         '<path d="m263 67 21-19 22 19v32h-43z" fill="#fae18a"/>'
         '<path d="M242 77h10v12h-10zm37-6h11v12h-11z" fill="#205b47"/>'
         '<path d="M226 100h85" stroke="#87cbb3" stroke-width="3"/>'),
    ]
    for slug, title, label, bg, accent, glass, shade, illustration in cards:
        body = rect(0, 0, 340, 130, bg, 'rx="10"')
        body += '<clipPath id="card"><rect width="340" height="130" rx="10"/></clipPath>'
        body += '<g clip-path="url(#card)">'
        body += f'<path d="M227 0h113v130H179Z" fill="{shade}"/>'
        body += f'<path d="M274 0h66v29l-62 37-73 64h-26l35-82Z" fill="{glass}"/>'
        body += f'<path d="M179 130 227 0m47 0-60 48 64 18 62-37m-62 37 62 38" fill="none" stroke="{bg}" stroke-width="3"/>'
        body += f'<circle cx="270" cy="75" r="47" fill="{bg}" stroke="{accent}" stroke-width="2"/>'
        body += illustration + '</g>'
        body += rect(1, 1, 338, 128, 'none', f'rx="9" stroke="{accent}" stroke-opacity=".55"')
        body += text(19, 58, title, 34, '#fff6eb', weight=700)
        body += text(20, 96, label, 25, accent, weight=600)
        body += f'<path d="M170 89h17m-6-6 6 6-6 6" fill="none" stroke="{accent}" stroke-width="2"/>'
        save(f'budget-{slug}.svg', 340, 130, title, f'查看{label}的推荐详情。', body)


def flybit_sample():
    rows = [
        ('美国', 564.36, '流畅', '#96e3ef'),
        ('日本', 340.81, '流畅', '#c0adff'),
        ('新加坡', 405.28, '流畅', '#a0e0b5'),
        ('香港', 456.43, '不可用', '#ffb68d'),
    ]
    w, h = 640, 420
    ink, muted, grid = '#182640', '#c6d8f0', '#405477'
    plot_x, plot_width = 130, 348
    body = rect(0, 0, w, h, ink, 'rx="14"')
    body += text(26, 48, 'FlyBit 晚高峰节点样本', 34, '#ffffff', weight=700)
    body += text(27, 83, '2026-08-13 晚间 · Siilas', 23, muted)
    body += text(plot_x, 123, '下行速度（Mbps）', 22, muted, weight=600)
    body += text(551, 123, 'ChatGPT', 23, muted, weight=600, extra='text-anchor="middle"')
    for tick in (0, 200, 400, 600):
        x = plot_x + plot_width * tick // 600
        body += line(x, 138, x, 365, grid)
        body += text(x, 395, str(tick), 21, muted, MONO, extra='text-anchor="middle"')
    for index, (region, speed, status, accent) in enumerate(rows):
        y = 150 + index * 55
        bar_width = round(plot_width * speed / 600, 2)
        body += text(26, y + 28, region, 25, '#ffffff', weight=600)
        body += rect(plot_x, y, bar_width, 38, accent, 'rx="5"')
        body += text(plot_x + bar_width - 11, y + 27, f'{speed:.2f}', 23, ink, MONO, 700,
                     'text-anchor="end"')
        body += rect(494, y, 114, 38, '#303b57', 'rx="19"')
        status_color = '#a0e0b5' if status == '流畅' else '#ffb68d'
        body += text(551, y + 27, status, 24, status_color, weight=700, extra='text-anchor="middle"')
    save('flybit-evening-sample.svg', w, h, 'FlyBit 晚高峰节点样本',
         '2026-08-13 晚间第三方记录。美国 564.36、日本 340.81、新加坡 405.28 Mbps，ChatGPT 流畅；香港 456.43 Mbps，ChatGPT 不可用。', body)


def sufe_outlets():
    rows = [
        ('普通机房', '1000 GB / 月', '9.9 元 / 月', '#303c72', '#c5d6ff',
         '<path d="M18 11h40v45H18z M18 26h40M18 41h40m-32-22h4m-4 15h4m-4 15h4"/>'),
        ('美国静态家宽', '250 GB / 月 · 固定住宅 IP', '20 元 / 月', '#71334b', '#ffccc4',
         '<path d="m14 32 24-21 24 21m-41-6v29h34V26M32 55V39h12v16"/>'),
        ('动态家宽', '30 元档为 420 GB / 月', '30–50 元 / 月', '#1e5149', '#b3f0cc',
         '<path d="M15 22h44m-9-9 9 9-9 9m9 13H15m9-9-9 9 9 9"/>'),
    ]
    w, h = 640, 407
    body = rect(0, 0, w, h, '#20203b', 'rx="14"')
    body += text(27, 49, '苏菲家宽 · 套餐与出口', 34, '#ffffff', weight=700)
    body += text(28, 84, '2026 年 5 月评测记录', 24, '#e0d9f1')
    for index, (name, quota, price, bg, accent, icon) in enumerate(rows):
        y = 108 + index * 94
        body += rect(20, y, 600, 82, bg, 'rx="10"')
        body += rect(20, y + 12, 4, 58, accent, 'rx="2"')
        body += f'<g transform="translate(37 {y + 8})" fill="none" stroke="{accent}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
        body += text(120, y + 34, name, 30, '#ffffff', weight=700)
        body += text(120, y + 66, quota, 23, accent)
        body += text(599, y + 50, price, 27, accent, weight=700, extra='text-anchor="end"')
    save('sufe-outlet-comparison.svg', w, h, '苏菲家宽套餐与出口',
         '2026 年 5 月评测记录：普通机房每月 9.9 元、1000 GB；美国静态家宽每月 20 元、250 GB；动态家宽每月 30 至 50 元，30 元档每月 420 GB。', body)


if __name__ == '__main__':
    featured(False)
    featured(True)
    rating_badges()
    mobile_routes()
    budget_cards()
    flybit_sample()
    sufe_outlets()
    print('Built 15 editorial SVG assets.')

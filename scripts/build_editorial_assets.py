"""Build the recommendation cards, mobile route cards and rating badges.

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


if __name__ == '__main__':
    featured(False)
    featured(True)
    rating_badges()
    mobile_routes()
    print('Built 9 editorial SVG assets.')

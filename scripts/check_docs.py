"""Check local Markdown links, GitHub-style heading anchors and SVG XML.

Standard library only; Python 3.9+. External URLs and network state are not checked.
"""
from collections import Counter
from html import unescape
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def prose(text):
    # Ignore fenced examples so their placeholder paths are not treated as links.
    return re.sub(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", "", text,
                  flags=re.MULTILINE | re.DOTALL)


def anchors(text):
    result = set(re.findall(r'\b(?:id|name)=[\"\']([^\"\']+)', text))
    seen = Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)(?:\s+#+)?\s*$', prose(text), re.MULTILINE):
        heading = re.sub(r'!?\[([^]]+)\]\([^)]*\)', r'\1', heading)
        heading = unescape(re.sub(r'<[^>]+>', '', heading)).lower()
        slug = re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')
        index = seen[slug]
        seen[slug] += 1
        result.add(f'{slug}-{index}' if index else slug)
    return result


def references(text):
    text = re.sub(r'`[^`\n]+`', '', prose(text))
    yield from re.findall(r'!?\[[^\]\n]*\]\(<?([^\s)>]+)>?(?:\s+"[^"]*")?\)', text)
    for key, value in re.findall(r'\b(href|src|srcset)=[\"\']([^\"\']+)[\"\']', text):
        if key == 'srcset':
            yield from (item.strip().split()[0] for item in value.split(',') if item.strip())
        else:
            yield value


def main():
    documents = sorted(p for p in ROOT.rglob('*.md') if '.git' not in p.parts)
    contents = {}
    errors = []
    for doc in documents:
        try:
            contents[doc] = doc.read_text(encoding='utf-8')
        except UnicodeError as error:
            errors.append(f'{doc.relative_to(ROOT)}: invalid UTF-8: {error}')

    count = 0
    for doc, text in contents.items():
        for href in references(text):
            parsed = urlsplit(unescape(href))
            if parsed.scheme or parsed.netloc:
                continue
            count += 1
            path = unquote(parsed.path)
            target = (doc.parent / path).resolve() if path else doc
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f'{doc.relative_to(ROOT)}: link leaves repository: {href}')
                continue
            if not target.exists():
                errors.append(f'{doc.relative_to(ROOT)}: missing target: {href}')
                continue
            if parsed.fragment and target.suffix.lower() == '.md' and target in contents:
                if unquote(parsed.fragment) not in anchors(contents[target]):
                    errors.append(f'{doc.relative_to(ROOT)}: missing anchor: {href}')

    vectors = sorted(ROOT.rglob('*.svg'))
    for vector in vectors:
        try:
            element = ET.parse(vector).getroot()
            if element.tag != '{http://www.w3.org/2000/svg}svg':
                errors.append(f'{vector.relative_to(ROOT)}: missing SVG namespace')
            if not element.get('viewBox'):
                errors.append(f'{vector.relative_to(ROOT)}: missing viewBox')
        except ET.ParseError as error:
            errors.append(f'{vector.relative_to(ROOT)}: invalid SVG: {error}')

    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Passed: {len(documents)} Markdown files, {count} local links, {len(vectors)} SVG files.')
    print('Scope: local links/anchors and SVG XML; external URLs, prices and service availability are not checked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

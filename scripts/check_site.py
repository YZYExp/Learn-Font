#!/usr/bin/env python3
"""Check generated HTML pages, local resources, and fragment targets without network access."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.references = []
        self.images = 0
        self.errors = []
        self.language = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang')
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.duplicates.append(attrs['id'])
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.references.append((tag, key, attrs[key]))
        if tag == 'img':
            self.images += 1
            if not attrs.get('alt'):
                self.errors.append('image has no descriptive alt text')

    handle_startendtag = handle_starttag


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', default='build/site')
    parser.add_argument('--output', help='Alias for the generated site directory')
    parser.add_argument('--base-path', help='Defaults to generated site-manifest.json')
    args = parser.parse_args()
    root = Path(args.output or args.directory).resolve()
    manifest_path = root / 'site-manifest.json'
    if not manifest_path.is_file():
        parser.error('site-manifest.json is missing; build the site first')
    manifest = json.loads(manifest_path.read_text())
    base = args.base_path or manifest['base_path']
    base = '/' + base.strip('/') + '/' if base.strip('/') else '/'
    pages = {}
    errors = []
    for file in sorted(root.rglob('*.html')):
        page = Page()
        page.feed(file.read_text(encoding='utf-8'))
        pages[file] = page
        errors.extend(f'{file.relative_to(root)}: duplicate id {item}' for item in page.duplicates)
        errors.extend(f'{file.relative_to(root)}: {item}' for item in page.errors)
        if not page.language:
            errors.append(f'{file.relative_to(root)}: document language is missing')
    if len(pages) != manifest['pages']:
        errors.append(f'Expected {manifest["pages"]} HTML pages, found {len(pages)}')
    checked = 0
    for file, page in pages.items():
        for tag, key, value in page.references:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path)
            if path.startswith('/'):
                if not path.startswith(base):
                    errors.append(f'{file.relative_to(root)}: URL does not use base path {base}: {value}')
                    continue
                target = root / path[len(base):]
            elif path:
                target = file.parent / path
            else:
                target = file
            target = target.resolve()
            if not target.is_relative_to(root):
                errors.append(f'{file.relative_to(root)}: local target escapes site: {value}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{file.relative_to(root)}: missing {tag}[{key}] {value}')
                continue
            fragment = unquote(parsed.fragment)
            if fragment and target.suffix == '.html':
                if target not in pages or fragment not in pages[target].ids:
                    errors.append(f'{file.relative_to(root)}: missing fragment in {value}')
            checked += 1
    epub = root / 'downloads/font-atlas.epub'
    if manifest['epub'] != epub.is_file():
        errors.append('EPUB availability differs from build manifest')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(pages)} pages, {checked} internal links/resources, '
          f'{sum(page.images for page in pages.values())} image references; base path {base}')


if __name__ == '__main__':
    main()

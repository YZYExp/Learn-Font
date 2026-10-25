#!/usr/bin/env python3
"""Build the reading site from the book's sole Markdown sources."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import markdown
from book_fingerprint import fingerprint

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/YZYExp/Learn-Font'
EXPORT_URL = REPOSITORY + '/actions/workflows/export.yml'


def esc(value):
    return html.escape(str(value), quote=True)


def normalize_base(value):
    if not value.startswith('/') or '?' in value or '#' in value or '..' in value.split('/'):
        raise ValueError('--base-path must be an absolute URL path without query, fragment, or ..')
    return '/' + value.strip('/') + '/' if value.strip('/') else '/'


class Rewriter(HTMLParser):
    """Rewrite local Markdown links and assets; retain Markdown-produced markup."""
    def __init__(self, source, routes, base):
        super().__init__(convert_charrefs=False)
        self.source, self.routes, self.base = source, routes, base
        self.output = []
        self.anchor_depth = 0

    def url(self, value):
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or value.startswith(('/', '#')):
            return value
        path = unquote(parsed.path)
        resolved = posixpath.normpath(posixpath.join(self.source.parent.as_posix(), path))
        if resolved.startswith('../'):
            raise ValueError(f'Link escapes project: {self.source}: {value}')
        if resolved in self.routes:
            target = self.routes[resolved]
        else:
            original = ROOT / resolved
            if not original.is_file():
                raise FileNotFoundError(f'{self.source}: local target not found: {value}')
            target = resolved
        return urlunsplit(('', '', self.base + quote(target, safe='/'), parsed.query, parsed.fragment))

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        for attr in ('href', 'src'):
            if data.get(attr):
                data[attr] = self.url(data[attr])
        if tag == 'table':
            self.output.append('<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的表格">')
        wrap = tag == 'img' and not self.anchor_depth
        if tag == 'img':
            data.setdefault('loading', 'lazy')
            data.setdefault('decoding', 'async')
            if wrap:
                self.output.append(f'<a class="figure-link" href="{esc(data["src"])}" target="_blank" rel="noopener" aria-label="{esc(data.get("alt", "插图"))}，打开原图">')
        self.output.append('<' + tag + ''.join(f' {key}="{esc(value)}"' if value is not None else f' {key}' for key, value in data.items()) + '>')
        if tag == 'a':
            self.anchor_depth += 1
        if wrap:
            self.output.append('</a>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.output.append(f'</{tag}>')
        if tag == 'a':
            self.anchor_depth -= 1
        if tag == 'table':
            self.output.append('</div>')

    def handle_data(self, data):
        self.output.append(data)

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

    def handle_comment(self, data):
        self.output.append('<!--' + data + '-->')


def excerpt(text):
    for paragraph in re.split(r'\n\s*\n', text):
        if paragraph.startswith(('#', '!', '*', '-', '|')):
            continue
        paragraph = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', paragraph)
        paragraph = re.sub(r'[`*_]', '', paragraph).strip()
        if paragraph:
            return paragraph[:110] + ('…' if len(paragraph) > 110 else '')
    return ''


def render_markdown(source, routes, base):
    text = (ROOT / source).read_text(encoding='utf-8')
    # The page header supplies the title. Keep all other content in source order.
    text = re.sub(r'\A\s*# [^\n]+\n', '', text, count=1)
    converter = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'], extension_configs={'toc': {'permalink': False}})
    markup = converter.convert(text)
    rewrite = Rewriter(Path(source), routes, base)
    rewrite.feed(markup)
    return ''.join(rewrite.output), converter.toc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-path', default='/')
    parser.add_argument('--output', default='build/site')
    parser.add_argument('--epub', type=Path, help='Copy an existing validated EPUB into the site')
    args = parser.parse_args()
    base = normalize_base(args.base_path)
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents and output in (ROOT / 'assets', ROOT / 'chapters', ROOT / 'site', ROOT / 'scripts'):
        parser.error('Refusing to replace a source directory')
    if output.exists() and any(output.iterdir()) and not (output / '.font-atlas-site').is_file():
        parser.error('Output exists and is not a previously generated site; choose an empty directory')
    if args.epub and not args.epub.is_file():
        parser.error(f'EPUB does not exist: {args.epub}')
    book = json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))
    chapters = book['chapters']
    extras = [*sorted((ROOT / 'appendices').glob('*.md')), *sorted((ROOT / 'references').glob('*.md'))]
    routes = {chapter['source']: chapter['slug'] + '/' for chapter in chapters}
    for source in extras:
        relative = source.relative_to(ROOT).as_posix()
        routes[relative] = source.relative_to(ROOT).with_suffix('').as_posix() + '/'
    if len(set(routes.values())) != len(routes):
        raise ValueError('Duplicate output routes')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / '.font-atlas-site').write_text('Generated by scripts/build_site.py\n')
    (output / '.nojekyll').write_text('')
    (output / 'assets').mkdir()
    for folder in ('images', 'designs'):
        source = ROOT / 'assets' / folder
        if source.exists():
            shutil.copytree(source, output / 'assets' / folder)
    for source in (ROOT / 'site').iterdir():
        if source.suffix in ('.css', '.js'):
            shutil.copy2(source, output / 'assets' / source.name)
    download = EXPORT_URL
    download_text = 'EPUB 导出入口'
    download_note = '网页可直接完整阅读；Actions 导出下载需登录 GitHub，产物保留30天。'
    valid_epub = bool(args.epub)
    metadata_path = args.epub.with_name('edition.json') if args.epub else None
    if metadata_path and metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        valid_epub = metadata.get('source_sha256') == fingerprint() and metadata.get('epub_sha256') == hashlib.sha256(args.epub.read_bytes()).hexdigest()
        if not valid_epub:
            print('EPUB snapshot differs from current source; using independent export workflow link.')
            download_note = '书稿已更新；请前往 Actions 获取导出产物，需登录 GitHub，保留30天。'
    if valid_epub:
        (output / 'downloads').mkdir()
        shutil.copy2(args.epub, output / 'downloads' / 'font-atlas.epub')
        download = base + 'downloads/font-atlas.epub'
        download_text = '下载 EPUB'
        download_note = '适合手机与电子书阅读器的离线阅读版本。'

    def url(route=''):
        return base + quote(route, safe='/')

    def header():
        return f'''<header class="site-header"><a class="brand" href="{url()}"><span class="brand-symbol" aria-hidden="true">字</span><span>{esc(book['title'])}<small>TYPE / FIELD NOTES</small></span></a><nav aria-label="主导航"><a href="{url()}#contents">目录</a><a href="{esc(download)}">{download_text}</a><a class="github" href="{REPOSITORY}">GitHub ↗</a></nav></header>'''

    def footer():
        return f'''<footer class="site-footer"><span>字的性格 · 字体、字形设计与文字排版图解</span><a href="{url('references/image-policy/')}">图片与字体来源</a><a href="{REPOSITORY}">源码与修订 ↗</a></footer>'''

    def layout(title, description, body, is_reader=False):
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="{esc(description)}"><title>{esc(title)} · {esc(book['title'])}</title><link rel="icon" href="{url('assets/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{url('assets/style.css')}"><script src="{url('assets/site.js')}" defer></script></head><body class="{'reader' if is_reader else 'home'}"><a class="skip-link" href="#main">跳至正文</a>{header()}{body}{footer()}</body></html>'''

    def sidebar(current):
        sections = []
        for part in book['parts']:
            links = ''.join(f'<li><a href="{url(ch["slug"] + "/")}"' + (' aria-current="page"' if current == ch['source'] else '') + f'><span>{index:02}</span>{esc(ch["title"])}</a></li>' for index, ch in enumerate(chapters, 1) if ch['part'] == part['id'])
            sections.append(f'<section><h3>{esc(part["title"])}</h3><ol>{links}</ol></section>')
        appendix_links = ''.join(f'<li><a href="{url(routes[path.relative_to(ROOT).as_posix()])}">{esc(path.read_text(encoding="utf-8").splitlines()[0].lstrip("#").strip())}</a></li>' for path in extras if path.parent.name == 'appendices')
        return '<aside class="reading-sidebar"><details class="chapter-menu" open><summary>全书目录 <span aria-hidden="true">＋</span></summary><nav aria-label="章节目录">' + ''.join(sections) + '<section><h3>附录</h3><ul>' + appendix_links + '</ul></section></nav></details></aside>'

    cards = []
    for part_index, part in enumerate(book['parts'], 1):
        entries = []
        for index, chapter in enumerate(chapters, 1):
            if chapter['part'] != part['id']:
                continue
            summary = excerpt((ROOT / chapter['source']).read_text(encoding='utf-8'))
            entries.append(f'''<a class="chapter-card" data-search="{esc(chapter['title'] + ' ' + summary)}" href="{url(chapter['slug'] + '/')}"><span class="chapter-number">{index:02}</span><div><h3>{esc(chapter['title'])}</h3><p>{esc(summary)}</p></div><span class="card-arrow" aria-hidden="true">↗</span></a>''')
        cards.append(f'<section class="part-section" data-part id="{esc(part["id"])}"><header><span class="part-index">0{part_index}</span><h2>{esc(part["title"].split("：", 1)[-1])}</h2></header><div class="chapter-grid">' + ''.join(entries) + '</div></section>')
    body = f'''<main id="main"><section class="hero"><div class="hero-copy"><p class="eyebrow">一本关于字的观察手册 · 开放阅读</p><h1>字的<span>性格</span><i aria-hidden="true">Aa</i></h1><p class="hero-subtitle">{esc(book['subtitle'])}</p><p class="hero-intro">从街角招牌到手机屏幕，从一笔一画到整页节奏。学会看见字的差异，理解设计的来历，再动手做一次。</p><div class="hero-actions"><a class="button primary" href="{url(chapters[0]['slug'] + '/')}">开始阅读 <span aria-hidden="true">→</span></a><a class="button secondary" href="{url('appendices/00-guide/')}">阅读导引</a></div><div class="book-facts"><span><strong>{len(book["parts"])}</strong> 篇学习路径</span><span><strong>{len(chapters)}</strong> 个完整章节</span><span>真实字体 · 对照图解</span></div></div><a class="cover-frame" href="{url(chapters[0]['slug'] + '/')}"><img src="{url(book['cover'])}" alt="字的性格书籍封面" fetchpriority="high"><span class="cover-caption">看见差异，然后理解设计。</span></a></section><section class="reading-line" aria-label="全书主线"><span>看见差异</span><b>→</b><span>理解来历</span><b>→</b><span>拆解结构</span><b>→</b><span>选择与组合</span><b>→</b><span>亲手设计</span></section><section class="contents" id="contents"><div class="contents-heading"><div><p class="eyebrow">CONTENTS / 阅读目录</p><h2>从观察到设计</h2></div><label class="search-box"><span class="sr-only">搜索章节标题或摘要</span><input id="chapter-search" type="search" placeholder="搜索：宋体、字距、品牌…" autocomplete="off"><span aria-hidden="true">⌕</span></label></div><p id="search-status" class="search-status" role="status" aria-live="polite">按顺序阅读，也可以从感兴趣的章节开始。</p>{''.join(cards)}<p id="no-results" hidden>没有找到相关章节。试试「排版」「字体」或其他关键词。</p></section><section class="extras"><div><p class="eyebrow">READ / MAKE / KEEP</p><h2>读过，也亲手试过。</h2><p>用术语表回查概念，跟随小项目把观察变成自己的设计判断。</p></div><div class="extra-links"><a href="{url('type-lab/')}">字体实验台 <span>→</span></a><a href="{url('appendices/01-glossary/')}">术语回查 <span>→</span></a><a href="{url('appendices/02-workbook/')}">可以做完的小项目 <span>→</span></a><a href="{esc(download)}">{download_text} <span>↗</span><small>{download_note}</small></a></div></section></main>'''
    (output / 'index.html').write_text(layout('字体、字形设计与文字排版图解', f'{len(book["parts"])}篇{len(chapters)}章，从字体识别到文字排版，以真实字体样张和原创图解学会观察、比较与设计。', body), encoding='utf-8')

    for source, route in routes.items():
        text = (ROOT / source).read_text(encoding='utf-8')
        markup, toc = render_markdown(source, routes, base)
        chapter = next((item for item in chapters if item['source'] == source), None)
        if chapter:
            index = chapters.index(chapter)
            title = chapter['title']
            part = next(item for item in book['parts'] if item['id'] == chapter['part'])
            eyebrow = f'{part["title"]} / {index + 1:02}'
            previous = chapters[index - 1] if index else None
            following = chapters[index + 1] if index + 1 < len(chapters) else None
        else:
            title = re.sub(r'^#\s*', '', text.splitlines()[0])
            eyebrow, previous, following = '阅读附录 / 资料', None, None
        nav = '<nav class="page-turn" aria-label="前后章节">'
        nav += f'<a href="{url(previous["slug"] + "/")}"><small>← 上一章</small><strong>{esc(previous["title"])}</strong></a>' if previous else f'<a href="{url()}#contents"><small>← 返回目录</small><strong>浏览全书</strong></a>'
        nav += f'<a href="{url(following["slug"] + "/")}"><small>下一章 →</small><strong>{esc(following["title"])}</strong></a>' if following else f'<a href="{url("appendices/02-workbook/")}"><small>继续练习 →</small><strong>可以做完的小项目</strong></a>'
        nav += '</nav>'
        article = f'''<div class="reading-progress" aria-hidden="true"><span></span></div><div class="reading-layout">{sidebar(source)}<main id="main" class="reading-main"><header class="article-header"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p class="reading-tip">插图完整展开 · 点击图片查看原图</p></header><article class="prose">{markup}</article>{nav}<a class="back-top" href="#main">回到本章开头 ↑</a></main></div>'''
        destination = output / route / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(layout(title, excerpt(text), article, True), encoding='utf-8')
    lab = output / 'type-lab'
    lab.mkdir()
    shutil.copy2(ROOT / 'site/type-lab.html', lab / 'index.html')
    (output / 'assets/fonts').mkdir()
    shutil.copy2(ROOT / 'assets/fonts/MozillaHeadline[wdth,wght].ttf', output / 'assets/fonts/headline.ttf')
    shutil.copy2(ROOT / 'assets/fonts/mozillaheadline-OFL.txt', output / 'assets/fonts/mozillaheadline-OFL.txt')
    (output / 'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#20443d"/><text x="32" y="46" font-size="43" text-anchor="middle" fill="#faf7ef" font-family="serif">字</text></svg>')
    (output / 'site-manifest.json').write_text(json.dumps({'base_path': base, 'chapters': len(chapters), 'pages': len(routes) + 2, 'epub': valid_epub}, ensure_ascii=False, indent=2))
    print(f'Built {len(routes) + 2} pages, {len(chapters)} chapters → {output}')


if __name__ == '__main__':
    main()

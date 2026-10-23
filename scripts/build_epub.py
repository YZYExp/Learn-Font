"""Build a reflowable EPUB 3 from the canonical chapter manifest."""
from pathlib import Path
import json,re,zipfile,html,datetime
import xml.etree.ElementTree as ET
import markdown
ROOT=Path(__file__).resolve().parents[1]
BOOK=json.loads((ROOT/'book.json').read_text())
OUT=ROOT/'build';OUT.mkdir(exist_ok=True)
CSS='''body{font-family:serif;line-height:1.8;margin:5%;color:#192c30}h1,h2,h3{line-height:1.4;break-after:avoid}h1{font-size:1.7em;margin-top:1.3em}h2{font-size:1.25em;margin-top:1.7em;color:#207b78}p{margin:.85em 0;text-align:justify}img{display:block;max-width:100%;height:auto;margin:1.3em auto}a{color:#207b78;overflow-wrap:anywhere}table{border-collapse:collapse;font-size:.85em;width:100%}td,th{border:1px solid #cfd5d0;padding:.4em;text-align:left}pre,code{font-family:monospace;white-space:pre-wrap;overflow-wrap:anywhere}blockquote{margin:1em 0;padding:.5em 1em;border-left:3px solid #207b78}li{margin:.4em 0}.cover{margin:0;padding:0}.cover img{max-height:95vh;margin:0 auto}.caption{color:#607174;font-size:.85em}'''
def esc(s):return html.escape(s,quote=True)
def xhtml(title,body):
 return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN"><head><title>'+esc(title)+'</title><link rel="stylesheet" type="text/css" href="style.css" /></head><body>'+body+'</body></html>'
def run():
 docs=[]
 docs.append(('cover','封面',xhtml('封面','<section class="cover"><img src="assets/images/cover.png" alt="字的性格封面" /></section>')))
 intro=ROOT/'appendices/00-guide.md'
 docs.append(('guide','阅读导引',xhtml('阅读导引',markdown.markdown(intro.read_text(),extensions=['tables','fenced_code']))))
 for c in BOOK['chapters']:
  s=(ROOT/c['source']).read_text()
  # Current chapters live beside one another; assets are under EPUB's OEBPS root.
  s=s.replace('../assets/','assets/')
  for other in BOOK['chapters']:
   s=s.replace(f"({Path(other['source']).name})",f"({other['id']}.xhtml)")
  body=markdown.markdown(s,extensions=['tables','fenced_code'])
  docs.append((c['id'],c['title'],xhtml(c['title'],body)))
 for p in sorted((ROOT/'appendices').glob('*.md')):
  if p==intro:continue
  s=p.read_text().replace('../assets/','assets/')
  docs.append(('app-'+p.stem,p.read_text().splitlines()[0].lstrip('# '),xhtml(p.stem,markdown.markdown(s,extensions=['tables','fenced_code']))))
 for id,t,s in docs:ET.fromstring(s)
 nav='<nav epub:type="toc" id="toc"><h1>目录</h1><ol>'+''.join(f'<li><a href="{id}.xhtml">{esc(t)}</a></li>' for id,t,s in docs)+'</ol></nav>'
 assets=list((ROOT/'assets/images').glob('*.png'))
 manifest=['<item id="css" href="style.css" media-type="text/css"/>','<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
 for id,t,s in docs:manifest.append(f'<item id="{id}" href="{id}.xhtml" media-type="application/xhtml+xml"/>')
 for i,p in enumerate(assets):manifest.append(f'<item id="im{i}" href="assets/images/{p.name}" media-type="image/png"'+(' properties="cover-image"' if p.name=='cover.png' else '')+'/>')
 opf='<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">urn:uuid:95e465a9-faa2-4ad4-9719-fd8432431480</dc:identifier><dc:title>字的性格：字体、字形设计与文字排版图解</dc:title><dc:language>zh-CN</dc:language><dc:creator>编写与图解：Codex</dc:creator><meta property="dcterms:modified">'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')+'</meta></metadata><manifest>'+''.join(manifest)+'</manifest><spine toc="ncx">'+''.join(f'<itemref idref="{id}"/>' for id,t,s in docs)+'</spine></package>'
 ncx='<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="urn:uuid:95e465a9-faa2-4ad4-9719-fd8432431480"/></head><docTitle><text>字的性格</text></docTitle><navMap>'+''.join(f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{esc(t)}</text></navLabel><content src="{id}.xhtml"/></navPoint>' for i,(id,t,s) in enumerate(docs,1))+'</navMap></ncx>'
 target=OUT/'字的性格.epub'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
  z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
  z.writestr('OEBPS/content.opf',opf);z.writestr('OEBPS/toc.ncx',ncx);z.writestr('OEBPS/nav.xhtml',xhtml('目录',nav));z.writestr('OEBPS/style.css',CSS)
  for id,t,s in docs:z.writestr(f'OEBPS/{id}.xhtml',s)
  for p in assets:z.write(p,'OEBPS/assets/images/'+p.name)
 with zipfile.ZipFile(target) as z:
  names=set(z.namelist())
  for n in names:
   if n.endswith(('.xhtml','.opf','.ncx','.xml')):ET.fromstring(z.read(n))
   if n.endswith('.xhtml'):
    root=ET.fromstring(z.read(n))
    for e in root.iter():
     for k in ['src','href']:
      v=e.get(k)
      if v and not v.startswith(('https:','http:','mailto:','#')):
       v=v.split('#')[0]
       from posixpath import normpath,join,dirname
       assert normpath(join(dirname(n),v)) in names,(n,v)
 print(f'{target}: {len(docs)} sections, {len(assets)} images; XML and packaged links valid')
if __name__=='__main__':run()

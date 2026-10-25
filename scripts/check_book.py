from pathlib import Path
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
b=json.loads((ROOT/'book.json').read_text())
count=0;images=set();links=set()
for c in b['chapters']:
 p=ROOT/c['source'];s=p.read_text();assert s.startswith('# '),p
 assert not re.search(r'TODO|待补图|图片占位|待撰写',s),p
 assert len(re.findall(r'[\u3400-\u9fff]',s))>=1000,(p,'too short')
 assert re.search(r'!\[.*?\]\(.+?\)',s),p
 assert 'https://' in s,p
 for alt,img in re.findall(r'!\[(.*?)\]\((.*?)\)',s):
  assert alt,(p,img);q=(p.parent/img).resolve();assert q.is_file(),q
  with Image.open(q) as im:im.verify()
  images.add(q)
 for link in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',s):
  if link.startswith(('https://','http://')):links.add(link)
  elif not link.startswith('#'):assert (p.parent/link.split('#')[0]).exists(),(p,link)
 count+=len(re.findall(r'[\u3400-\u9fff]',s))
ids=[c['id'] for c in b['chapters']]
assert len(ids)==len(set(ids)), 'duplicate chapter IDs'
assert len({c['slug'] for c in b['chapters']})==len(ids), 'duplicate routes'
assert [id for part in b['parts'] for id in part['chapters']]==ids, 'part order differs from reading order'
for part in b['parts']:
 for id in part['chapters']:
  assert next(c for c in b['chapters'] if c['id']==id)['part']==part['id']
print(json.dumps({'chapters':len(b['chapters']),'han_characters':count,'chapter_images':len(images),'source_urls':len(links)},ensure_ascii=False))

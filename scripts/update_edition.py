from pathlib import Path
import json,hashlib,datetime
from book_fingerprint import ROOT,fingerprint
p=ROOT/'downloads/font-atlas.epub'
(ROOT/'downloads/edition.json').write_text(json.dumps({'edition':datetime.date.today().isoformat(),'source_sha256':fingerprint(),'epub_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')

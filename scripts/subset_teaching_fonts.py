"""Optional size reduction from full original Noto CJK fonts.
Usage: python scripts/subset_teaching_fonts.py /path/to/original-font-directory
Bundled subsets already contain the glyphs needed to rebuild this edition's figures.
"""
from pathlib import Path
import sys,json,hashlib
from fontTools import subset
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parents[1]
def run(original_dir):
 corpus=''.join(p.read_text() for folder in ['chapters','appendices','scripts','references'] for p in (ROOT/folder).glob('*') if p.suffix in ['.md','.py','.json'])+(ROOT/'book.json').read_text()
 codes=set(map(ord,corpus))|set(range(32,768))|set(range(0x3000,0x3100))
 records=[]
 for n,alias in [('NotoSerifCJKsc-Regular.otf','BookSpecimenSerifSC'),('NotoSerifCJKtc-Regular.otf','BookSpecimenSerifTC'),('NotoSerifCJKjp-Regular.otf','BookSpecimenSerifJP')]:
  src=Path(original_dir)/n;f=TTFont(src)
  records.append({'file':n,'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'original_names':{str(i):f['name'].getDebugName(i) for i in [1,2,4,5,6]},'subset_family':alias})
  opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];opt.name_legacy=True;opt.name_languages=['*'];opt.recalc_timestamp=False
  sub=subset.Subsetter(options=opt);sub.populate(unicodes=codes);sub.subset(f)
  for rec in f['name'].names:
   if rec.nameID in [1,3,4,6,16,18]:
    value=alias if rec.nameID!=3 else alias+'-TeachingSubset'
    rec.string=value.encode(rec.getEncoding())
  f.save(ROOT/'assets/fonts'/n)
 (ROOT/'references/font-subsets.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
 print('Saved teaching subsets; preserve OFL and original attribution.')
if __name__=='__main__':run(sys.argv[1])

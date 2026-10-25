"""Fingerprint only the inputs used by the EPUB, independently of website code."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
def fingerprint():
 paths=[ROOT/'book.json']
 for name,pattern in [('chapters','*.md'),('appendices','*.md'),('assets/images','*.png'),('assets/designs','*')]:
  paths.extend(p for p in (ROOT/name).rglob(pattern) if p.is_file())
 h=hashlib.sha256()
 for p in sorted(paths):
  h.update(p.relative_to(ROOT).as_posix().encode());h.update(b'\0');h.update(p.read_bytes());h.update(b'\0')
 return h.hexdigest()
if __name__=='__main__':print(fingerprint())

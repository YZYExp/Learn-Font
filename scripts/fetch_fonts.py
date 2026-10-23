"""Fetch optional, unmodified specimen fonts excluded from distribution.
Their license notices are kept in assets/fonts/. Network is needed only here.
"""
from pathlib import Path
import hashlib,json
import requests
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'assets/fonts'
URW=['NimbusRoman-Regular.otf','P052-Roman.otf','C059-Roman.otf','NimbusSans-Regular.otf','URWGothic-Book.otf','NimbusSansNarrow-Regular.otf','Z003-MediumItalic.otf']
URLS={n:'https://raw.githubusercontent.com/ArtifexSoftware/urw-base35-fonts/master/fonts/'+n for n in URW}
URLS.update({n:'https://mirrors.ctan.org/fonts/fandol/'+n for n in ['FandolKai-Regular.otf','FandolFang-Regular.otf']})
def main():
 for name,url in URLS.items():
  dest=F/name
  if dest.exists():continue
  r=requests.get(url,timeout=90);r.raise_for_status()
  if r.content[:4] not in (b'OTTO',b'\x00\x01\x00\x00'):raise ValueError(f'Not a font: {name}')
  dest.write_bytes(r.content);print(name,len(r.content))
if __name__=='__main__':main()

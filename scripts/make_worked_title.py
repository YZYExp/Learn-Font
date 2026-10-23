"""A complete original, editable four-character geometric lettering exercise."""
from pathlib import Path
from PIL import ImageDraw
from make_figures import base,panel,text,wrap,OUT,INK,TEAL,ROOT
# Coordinates are original centre-line drawings in a 100 x 130 field.
PATHS={
'日': [[(10,5),(90,5),(90,125),(10,125),(10,5)],[(10,65),(90,65)]],
'月': [[(10,130),(20,5),(90,5),(90,125),(70,125)],[(17,48),(90,48)],[(14,88),(90,88)]],
'山': [[(12,50),(12,120),(90,120),(90,50)],[(51,5),(51,120)]],
'水': [[(50,5),(50,125),(35,115)],[(8,45),(37,45),(8,100)],[(90,35),(65,60),(93,105)]]}
def glyph(d,char,x,y,scale,weight,refine=False):
 for i,path in enumerate(PATHS[char]):
  w=weight
  if refine and ((char=='日' and i==1) or (char=='月' and i>0)):w=weight*.75
  d.line([(x+px*scale,y+py*scale) for px,py in path],fill=INK,width=max(1,round(w*scale)),joint='curve')
def main():
 im,d=base(27,'完整示范：从四个骨架到一组标题')
 for i,(label,weight,refine) in enumerate([('A  日月山水：先确定四个字的可识读骨架',2,False),('B  加入共同笔画厚度，观察密字与疏字',15,False),('C  内部横画略轻：一个可继续修订的候选方案',15,True)]):
  yy=panel(d,246+i*350,label,310)
  for j,c in enumerate('日月山水'):glyph(d,c,105+j*235,yy+4,1.35,weight,refine)
 text(d,(92,1322),'四字均为本书原创几何字形；不是成品字体或通用参数。',26,'cn',TEAL)
 im.save(OUT/'fig-27-extra.png',optimize=True)
 target=ROOT/'assets/designs';target.mkdir(exist_ok=True)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="250" viewBox="0 0 960 250"><title>日月山水：可编辑原创几何字形</title><rect width="960" height="250" fill="#f5f1e9"/>']
 for j,c in enumerate('日月山水'):
  for i,path in enumerate(PATHS[c]):
   points=' '.join(f'{105+j*235+x*1.35},{30+y*1.35}' for x,y in path)
   w=15*.75 if ((c=='日' and i==1) or (c=='月' and i>0)) else 15
   svg.append(f'<polyline points="{points}" fill="none" stroke="#192c30" stroke-width="{w*1.35}" stroke-linejoin="round"/>')
 svg.append('</svg>');(target/'riyueshanshui.svg').write_text(''.join(svg))
 print('Rendered worked-title example and editable SVG')
if __name__=='__main__':main()

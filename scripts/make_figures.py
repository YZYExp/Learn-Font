"""Render verifiable specimens with bundled fonts; original diagrams are labelled."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math
ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'assets/fonts'; OUT=ROOT/'assets/images'; OUT.mkdir(exist_ok=True)
W,H=1120,1480
BG='#f5f1e9'; INK='#192c30'; MUTED='#607174'; RED='#b54d38'; TEAL='#207b78'; LINE='#d6d9d1'
fonts={'cn':'NotoSansSC-Regular.ttf','song':'NotoSerifCJKsc-Regular.otf','jp':'NotoSerifCJKjp-Regular.otf','tc':'NotoSerifCJKtc-Regular.otf','sans':'DejaVuSans.ttf','bold':'DejaVuSans-Bold.ttf','serif':'DejaVuSerif.ttf','mono':'DejaVuSansMono.ttf','roman':'NimbusRoman-Regular.otf','human':'P052-Roman.otf','clar':'C059-Roman.otf','neo':'NimbusSans-Regular.otf','geo':'URWGothic-Book.otf','narrow':'NimbusSansNarrow-Regular.otf','kai':'FandolKai-Regular.otf','fang':'FandolFang-Regular.otf'}
def font(key,size):return ImageFont.truetype(str(F/fonts[key]),size)
def text(d,xy,s,size=30,key='cn',fill=INK):d.text(xy,s,font=font(key,size),fill=fill,anchor='lt')
def wrap(d,xy,s,width=930,size=29,key='cn',fill=INK,gap=13):
 x,y=xy;line=''
 for c in s:
  if c=='\n' or d.textlength(line+c,font=font(key,size))>width:
   text(d,(x,y),line,size,key,fill);y+=size+gap;line='' if c=='\n' else c
  else:line+=c
 if line:text(d,(x,y),line,size,key,fill)
 return y+size+gap
def specimen(d,s,y,key='cn',size=94,x=92,width=930,fill=INK):
 while d.textlength(s,font=font(key,size))>width:size-=1
 text(d,(x,y),s,size,key,fill)
def base(n,title,kicker='TYPE / FIELD NOTES'):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 text(d,(66,52),f'{n:02d}   /   {kicker}',23,'sans',TEAL)
 wrap(d,(64,109),title,990,48)
 d.line((64,209,1056,209),fill=INK,width=2)
 text(d,(66,1423),'字的性格  /  真实字体排印 · 原创教学图解',24,'cn',MUTED)
 return im,d
def panel(d,y,label,height=300):
 d.rounded_rectangle((64,y,1056,y+height),18,fill='#fffdf8')
 text(d,(90,y+24),label,27,'cn',TEAL)
 return y+82
def save(im,n):im.save(OUT/f'fig-{n:02}.png',optimize=True)
def para(d,x,y,width,size=28,leading=45,lines=5,key='cn'):
 s='清晨，沿着街道看字。招牌、书页与屏幕各有节奏，文字也在组织我们的目光。'
 line='';row=0
 for c in s*8:
  if d.textlength(line+c,font=font(key,size))>width and c not in '，。！？；：、）》」』】':
   text(d,(x,y+row*leading),line,size,key);row+=1;line=c
   if row>=lines:break
  else:line+=c

def main():
 for n in range(1,31):
  title=json.loads((ROOT/'book.json').read_text())['chapters'][n-1]['title']
  im,d=base(n,title)
  if n==1:
   for y,label,key in [(246,'A  Noto Serif CJK SC Regular / 宋体','song'),(650,'B  Noto Sans SC Regular / 黑体','cn')]:
    yy=panel(d,y,label,360);specimen(d,'清风入书页',yy,key,126);wrap(d,(92,yy+166),'永  国  三  人  心  字',900,56,key)
   wrap(d,(90,1070),'保持文字与字号相同，比较横竖粗细、笔画末端和字内留白。两套字体的字面与黑度并不完全一致。',930,32)
  elif n==4:
   for i,(label,k,word,desc) in enumerate([
    ('A  书写：观察笔锋与转折','kai','永和九年','FandolKai / 现代字体样张，非历史手迹'),
    ('B  印刷：观察横竖对比与末端','song','永和九年','Noto Serif CJK SC / 非历史刻本复刻'),
    ('C  屏幕：观察连续排印的稳定性','cn','永和九年','Noto Sans SC / 同文比较，不代表单线进化')]):
    yy=panel(d,246+i*350,label,310);specimen(d,word,yy,k,125);text(d,(98,yy+170),desc,26,'cn',MUTED)
  elif n==7:
   yy=panel(d,246,'A  放大末端：Noto Serif CJK SC Regular',520)
   specimen(d,'三 永',yy,'song',255)
   wrap(d,(98,yy+320),'看横画收尾、撇捺与粗细变化；不是每一笔都使用同一种末端。',910,30)
   yy=panel(d,806,'B  回到正文：大字特征是否仍然清楚？',430)
   para(d,98,yy,900,36,62,4,'song')
  elif n==2:
   yy=panel(d,246,'A  一套字体：相同规则作用于不同的字',320)
   specimen(d,'字的性格  文字设计',yy,'song',94)
   yy=panel(d,606,'B  现成字形的字标编排：只处理这一组字母',370)
   text(d,(105,yy),'AV',210,'sans');d.line((110,yy+210,460,yy+210),fill=RED,width=9)
   wrap(d,(560,yy+5),'DejaVu Sans 加线条的原创编排。一个字标不等于可连续排正文的字体。',420,33)
   wrap(d,(90,1060),'书法和手写还包含书写工具、动作与时间。字体可以吸收这些特征，概念仍需分开。',930,32)
  elif n==3:
   yy=panel(d,246,'A  拉丁字母：看高度，也看基线',470)
   f=font('serif',180);baseline=yy+280
   d.text((92,baseline),'H x g p',font=f,anchor='ls',fill=INK)
   for v,l in [(baseline+f.getbbox('H',anchor='ls')[1],'大写高度'),(baseline+f.getbbox('x',anchor='ls')[1],'x 字高'),(baseline,'基线'),(baseline+f.getbbox('g',anchor='ls')[3],'下伸部')]:
    d.line((90,v,800,v),fill=TEAL,width=2);text(d,(820,v-10),l,23,'cn',TEAL)
   yy=panel(d,752,'B  中文：笔画、重心和空间一起看',440)
   specimen(d,'永 国 心',yy,'song',180)
   wrap(d,(92,yy+235),'先描述看得见的位置与形状，再判断风格。标线仅用于本例观察，不代表所有字体共享同一数值。',915,28)
  elif n==5:
   for i,(label,k,word,desc) in enumerate([
    ('A  大写字母的比例与衬线','roman','ROMAN LETTERS','Nimbus Roman / 当代字体回看字形结构'),
    ('B  小写、升部与降部','roman','reading type','同一字体的小写系统；非历史文献摹本'),
    ('C  连续排印中的字宽变化','human','minimum / WWW','P052 Roman / 对照字母与词的视觉节奏')]):
    yy=panel(d,246+i*350,label,310);specimen(d,word,yy,k,93);text(d,(98,yy+145),desc,26,'cn',MUTED)
  elif n in [10,11]:
   keys=['roman','human','clar'] if n in [5,10] else ['sans','neo','geo']
   names=[fonts[k].split('.')[0] for k in keys]
   for i,(k,name) in enumerate(zip(keys,names)):
    yy=panel(d,246+i*352,f'{chr(65+i)}  {name}',318)
    specimen(d,'Hamburgefonts',yy,k,105);specimen(d,'a g R 012345',yy+128,k,65)
  elif n==6:
   yy=panel(d,246,'A  低分辨率采样：放大像素，不等于笔画设计',470)
   tiny=Image.new('RGB',(70,35),'white');td=ImageDraw.Draw(tiny);td.text((0,0),'Aa',font=font('serif',32),fill=INK,anchor='lt')
   im.paste(tiny.resize((700,350),Image.Resampling.NEAREST),(100,yy+4))
   yy=panel(d,752,'B  同一字体在较大尺寸重新栅格化',450)
   specimen(d,'Aa',yy,'serif',260)
   wrap(d,(580,yy+18),'数字轮廓经过渲染，才成为屏幕上的像素。此图为分辨率原理示意。',410,31)
  elif n==8:
   yy=panel(d,246,'A  中文黑体：Noto Sans SC Regular',300);specimen(d,'城市与文字',yy,'cn',130)
   for y,k,l in [(590,'sans','B  DejaVu Sans Regular'),(940,'bold','C  DejaVu Sans Bold')]:
    yy=panel(d,y,l,310);specimen(d,'Same family',yy,k,118)
   text(d,(92,1320),'B、C 是同家族字重对照；A 不是 B、C 的中文版本。',27,'cn',MUTED)
  elif n==9:
   avail=(F/fonts['kai']).exists() and (F/fonts['fang']).exists()
   for i,(k,l) in enumerate([('kai','A  FandolKai Regular / 楷体'),('fang','B  FandolFang Regular / 仿宋'),('song','C  Noto Serif CJK SC / 宋体')] if avail else [('song','A  宋体参照（非楷体）'),('cn','B  黑体参照（非仿宋）')]):
    yy=panel(d,246+i*350,l,310);specimen(d,'永和九年 清风入林',yy,k,87)
  elif n==12:
   for i,k in enumerate(['mono','sans','geo']):
    yy=panel(d,246+i*350,['A  DejaVu Sans Mono / 等宽','B  DejaVu Sans / 比例','C  URW Gothic / 几何倾向'][i],310)
    specimen(d,'iiii WWWW 0123',yy,k,90)
    if i<2:
     specimen(d,'1111 8888 0000',yy+120,k,70)
  elif n==13:
   for i,(k,l) in enumerate([('song','A  Noto Serif CJK SC / 简体中文地区字形'),('tc','B  Noto Serif CJK TC / 台湾地区字形'),('jp','C  Noto Serif CJK JP / 日本地区字形')]):
    yy=panel(d,246+i*350,l,310);specimen(d,'骨 直 令 返',yy,k,135)
   text(d,(92,1328),'同一码位、不同地区字体；仅这四字，不据此概括全部字形。',25,'cn',MUTED)
  elif n==14:
   yy=panel(d,246,'A  中心路径 / B  给路径增加宽度（原创几何示意）',450)
   for x,width,color in [(210,5,TEAL),(690,54,INK)]:
    d.line([(x,yy+230),(x+90,yy),(x+180,yy+230)],fill=color,width=width)
    d.line((x+40,yy+140,x+140,yy+140),fill=color,width=width)
   yy=panel(d,736,'C  最终轮廓可以脱离等宽描边继续调整',450)
   d.polygon([(200,yy+230),(300,yy),(365,yy),(480,yy+230),(415,yy+230),(332,yy+57),(250,yy+230)],fill=INK)
   d.rectangle((270,yy+140,405,yy+174),fill=INK)
   wrap(d,(570,yy+12),'路径解释笔画走向；轮廓决定黑白边界。真实字体还要处理交接、粗细和视觉平衡。',390,33)
  elif n==15:
   yy=panel(d,246,'A  相同外框内，不同字形的空间不同',460)
   for x,s in [(140,'国'),(570,'心')]:
    d.rectangle((x,yy,x+300,yy+300),outline=TEAL,width=3);specimen(d,s,yy+35,'song',250,x=x+25,width=275)
   yy=panel(d,746,'B  同一字，改变大小与位置（排版模拟）',470)
   for x,size,dy in [(135,210,18),(590,245,-2)]:
    d.rectangle((x,yy,x+300,yy+300),outline=TEAL,width=3);specimen(d,'国',yy+dy,'song',size,x=x+25,width=280)
   text(d,(95,1268),'不要把字面大小、中宫疏密、字号当成同一个量。',30,'cn',MUTED)
  elif n==16:
   yy=panel(d,246,'A  几何等高：圆在平直边界旁的视觉关系',420)
   d.rectangle((180,yy+20,390,yy+250),fill=INK);d.ellipse((620,yy+20,850,yy+250),fill=INK)
   for y in [yy+20,yy+250]:d.line((100,y,1000,y),fill=TEAL,width=2)
   yy=panel(d,706,'B  让曲线略微越界（幅度夸张的教学示意）',470)
   d.rectangle((180,yy+20,390,yy+250),fill=INK);d.ellipse((620,yy+6,850,yy+264),fill=INK)
   for y in [yy+20,yy+250]:d.line((100,y,1000,y),fill=TEAL,width=2)
   text(d,(95,1250),'这不是规定比例；实际修正需在目标字号下反复测试。',28,'cn',MUTED)
  elif n==17:
   for i,(feat,l) in enumerate([(['-kern'],'A  关闭字体自带 kerning'),(['kern'],'B  开启字体自带 kerning')]):
    yy=panel(d,246+i*420,l,370)
    d.text((100,yy),'AVATAR To',font=font('serif',135),features=feat,fill=INK,anchor='lt')
   wrap(d,(95,1160),'同一字体、同一字号。观察 AV 与 To 的局部关系；字偶调整与整段统一加字距是两种操作。',920,32)
  elif n==18:
   for i,(k,l) in enumerate([('sans','A  DejaVu Sans Regular'),('bold','B  DejaVu Sans Bold'),('narrow','C  Nimbus Sans Narrow / 另一家族')]):
    yy=panel(d,246+i*350,l,310);specimen(d,'Type family 2026',yy,k,96)
   text(d,(92,1320),'C 演示宽度差异，不冒充 DejaVu 家族的宽度轴。',28,'cn',MUTED)
  elif n==19:
   yy=panel(d,246,'A  导视：先看见目的地',300);specimen(d,'阅览室  →',yy,'cn',145)
   yy=panel(d,586,'B  书页：维持连续阅读',300);para(d,96,yy,900,32,52,3,'song')
   yy=panel(d,926,'C  界面：短标签与状态清楚',310);specimen(d,'保存草稿',yy,'cn',64);text(d,(98,yy+108),'已保存于本机  ·  继续编辑',32,'cn',MUTED)
  elif n==20:
   for i,(c,e,l) in enumerate([('song','serif','A  中文宋体 + 拉丁衬线'),('cn','sans','B  中文黑体 + 拉丁无衬线'),('song','sans','C  中文宋体 + 拉丁无衬线')]):
    yy=panel(d,246+i*350,l,310);specimen(d,'清风书店',yy,c,95);specimen(d,'BOOKS / Reading room',yy+120,e,54)
  elif n==21:
   for i,(size,leading,l) in enumerate([(34,38,'A  较紧行距'),(34,60,'B  同字号，增加行距')]):
    yy=panel(d,246+i*500,l,460);para(d,96,yy,900,size,leading,6,'song')
   text(d,(92,1320),'对照仅改变行距；舒适度还受行长、字体和设备影响。',27,'cn',MUTED)
  elif n==22:
   yy=panel(d,246,'A  所有信息同样重',420)
   for i,s in enumerate(['清风读书会','城市中的文字','周六 14:00 · 二层阅览室','报名后到场即可参加']):text(d,(98,yy+i*65),s,38)
   yy=panel(d,706,'B  根据阅读顺序建立层级',540)
   text(d,(98,yy),'清风读书会',30,'cn',TEAL);text(d,(98,yy+76),'城市中的文字',72,'song');text(d,(98,yy+207),'周六 14:00 · 二层阅览室',39);text(d,(98,yy+286),'报名后到场即可参加',29,'cn',MUTED)
  elif n in [23,29]:
   yy=panel(d,246,'A  一份样张：大字、正文、数字和标点',470)
   specimen(d,'清风入书页',yy,'song',112);para(d,96,yy+155,910,31,48,3,'song');text(d,(98,yy+325),'0123456789  Aa Bb  ，。！？「」',38)
   yy=panel(d,756,'B  转入真实尺寸应用：活动卡片（原创）',480)
   text(d,(100,yy),'READING / 2026',25,'sans',TEAL);text(d,(100,yy+65),'周末读字',83,'song');text(d,(100,yy+190),'14:00  →  二层阅览室',42)
   text(d,(100,yy+300),'先测试信息是否找得到，再增加装饰。',30,'cn',MUTED)
  elif n==24:
   yy=panel(d,246,'A  常规排印可以组织品牌语气',350)
   text(d,(96,yy),'清风',118,'song');text(d,(450,yy+12),'READING ROOM',45,'sans');text(d,(450,yy+89),'书与城市之间',37)
   yy=panel(d,636,'B  现成字形的字标排版练习（原创编排）',430)
   text(d,(98,yy),'AV',190,'sans');d.line((98,yy+193,420,yy+193),fill=TEAL,width=9)
   wrap(d,(560,yy+8),'示例用于分辨字标与通用字体。本图不复制或代表任何真实品牌。',390,34)
   wrap(d,(92,1130),'品牌字体需要面对整套语言、信息层级、屏幕与印刷条件，不只解决一个大标题。',930,31)
  elif n==25:
   yy=panel(d,246,'A  近看：方向与目的地',430);specimen(d,'阅览室 →',yy,'cn',148)
   text(d,(100,yy+210),'READING ROOM   /   2F',35,'sans',MUTED)
   yy=panel(d,716,'B  缩小模拟：先检验什么信息还剩下',450)
   specimen(d,'阅览室 →',yy+30,'cn',68)
   text(d,(100,yy+148),'READING ROOM   /   2F',18,'sans',MUTED)
   wrap(d,(98,yy+240),'缩小不能代替真实距离和环境测试；它能先暴露层级不足。',900,31)
  elif n==26:
   mfiles=list(F.glob('Mozilla*.ttf'))+list(F.glob('Mozilla*.otf'))
   yy=panel(d,246,'A  真实品牌字体样张 / 见本章官方来源',390)
   if mfiles:
    mf=ImageFont.truetype(str(mfiles[0]),88);d.text((98,yy),'Mozilla / Open web',font=mf,fill=INK,anchor='lt')
    text(d,(98,yy+145),mfiles[0].stem[:43],26,'sans',MUTED)
   else:
    specimen(d,'Aa / Brand voice',yy,'sans',102);text(d,(98,yy+145),'原创练习，非任何品牌的官方字样',29,'cn',MUTED)
   yy=panel(d,676,'B  将观察转成练习：同内容，不同语气',470)
   specimen(d,'Open for everyone',yy,'serif',85);specimen(d,'Open for everyone',yy+145,'bold',85)
   text(d,(98,yy+290),'B 使用 DejaVu，非 Mozilla 或 IBM 官方排版。',27,'cn',MUTED)
  elif n==27:
   for i,(label,thick,inside) in enumerate([('A  原创练习：日字骨架',4,0),('B  为骨架增加等宽笔画',28,0),('C  调整内部横画与留白，再测试',28,7)]):
    yy=panel(d,246+i*350,label,310)
    x=125;y=yy;ww=150;hh=180
    d.rectangle((x,y,x+ww,y+hh),outline=INK,width=thick)
    d.line((x,y+hh//2+inside,x+ww,y+hh//2+inside),fill=INK,width=thick if i<2 else 22)
    wrap(d,(400,yy+10),['只画外框与中横的走向，先保证可识读。','加粗会挤压内部空间，不能只看外轮廓。','调整只是一个候选方案，需放进日期与标题继续检验。'][i],590,31)
   text(d,(92,1320),'几何日字为本书原创，不是从楷体自动生成宋体的流程。',27,'cn',MUTED)
  elif n==28:
   yy=panel(d,246,'A  节点、控制柄与曲线（原创三次贝塞尔示意）',600)
   p0=(150,yy+320);p1=(300,yy-10);p2=(740,yy+420);p3=(930,yy+30)
   d.line([p0,p1],fill=RED,width=3);d.line([p2,p3],fill=RED,width=3)
   pts=[]
   for i in range(101):
    t=i/100;pts.append(tuple((1-t)**3*p0[j]+3*(1-t)**2*t*p1[j]+3*(1-t)*t*t*p2[j]+t**3*p3[j] for j in [0,1]))
   d.line(pts,fill=INK,width=10)
   for i,(x,y) in enumerate([p0,p1,p2,p3]):d.ellipse((x-10,y-10,x+10,y+10),fill=RED);text(d,(x+12,y+15),f'P{i}',25,'sans',RED)
   yy=panel(d,886,'B  修改之后必须回到字与词的测试',350)
   specimen(d,'曲线 → 字形 → 词组',yy,'cn',65)
   text(d,(98,yy+130),'平滑节点只是工具状态，不自动保证轮廓好看。',30)
  elif n==30:
   for i,(s,l,desc) in enumerate([('U+0041','A  字符：抽象文字单位的编码','例如拉丁大写 A；字符不等于某一种外形。'),('A A A','B  字形：字体内的具体视觉形态','同一字符可以对应不同字形与替代形式。'),('OTF / TTF','C  字体文件：轮廓、映射与排版信息','扩展名不能单独判断质量或使用授权。')]):
    yy=panel(d,246+i*350,l,310);specimen(d,s,yy,'serif' if i==1 else 'mono',96);text(d,(98,yy+135),desc,26,'cn',MUTED)
  save(im,n)
 # Cover: exact typography, no synthetic glyphs.
 im=Image.new('RGB',(1200,1800),INK);d=ImageDraw.Draw(im)
 text(d,(92,95),'TYPE / FORM / READING',28,'sans','#8fc7bc')
 text(d,(80,250),'字的',205,'song','#f5f1e9');text(d,(80,500),'性格',205,'cn','#f5f1e9')
 d.line((92,812,1108,812),fill='#8fc7bc',width=4)
 text(d,(94,865),'字体、字形设计与文字排版图解',44,'cn','#f5f1e9')
 text(d,(81,1070),'Aa',310,'serif','#d57d54');text(d,(635,1140),'永',240,'song','#8fc7bc')
 text(d,(94,1610),'看见差异 · 理解结构 · 学会设计',35,'cn','#f5f1e9')
 im.save(OUT/'cover.png',optimize=True)
 print('Rendered 30 chapter figures and cover')
if __name__=='__main__':main()

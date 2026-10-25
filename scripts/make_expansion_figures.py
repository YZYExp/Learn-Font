"""Rebuild second-edition instructional cards using real font shaping.

No generated text images. Pixel settings are controlled teaching examples,
not prescriptions. Optional source fonts and licenses: expansion-fonts.json.
"""
from pathlib import Path
from io import BytesIO
import json, hashlib
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT=Path(__file__).resolve().parents[1]; F=ROOT/'assets/fonts'; OUT=ROOT/'assets/images'
BG='#f5f1e9'; INK='#192c30'; TEAL='#207b78'; RED='#b54d38'; MUTED='#607174'; PAPER='#fffdf8'; LINE='#d6d9d1'
NAMES={'cn':'NotoSansSC-Regular.ttf','song':'NotoSansSC-Regular.ttf','sans':'DejaVuSans.ttf','mono':'DejaVuSansMono.ttf','source':'SourceSerif4Variable-Roman.otf','plex':'IBMPlexSans-Regular.ttf','practice':'PracticeGridAtlas-Regular.ttf'}
FONT_BUFFERS={}; USED=set(); CMAPS={}
def ft(key,size,axes=None):
 name=NAMES.get(key,key); USED.add(name)
 if name not in CMAPS: CMAPS[name]=TTFont(F/name).getBestCmap()
 if axes:
  tag=(name,tuple(sorted(axes.items())))
  if tag not in FONT_BUFFERS:
   f=instantiateVariableFont(TTFont(F/name),axes,inplace=False);b=BytesIO();f.save(b);FONT_BUFFERS[tag]=b.getvalue()
  return ImageFont.truetype(BytesIO(FONT_BUFFERS[tag]),size)
 return ImageFont.truetype(str(F/name),size)
def tx(d,x,y,s,size=28,key='cn',color=INK,axes=None,features=None,anchor='lt'):
 font=ft(key,size,axes)
 missing={ch for ch in s if not ch.isspace() and ord(ch) not in CMAPS[NAMES.get(key,key)]}
 if missing: raise ValueError(f"Missing glyphs in {key}: {missing}")
 d.text((x,y),s,font=font,fill=color,anchor=anchor,features=features)
 return d.textlength(s,font=font,features=features)
def wrap(d,x,y,s,width=900,size=29,color=INK,key='cn',leading=None):
 leading=leading or size+16;line=''
 for ch in s:
  if ch=='\n' or d.textlength(line+ch,font=ft(key,size))>width:
   tx(d,x,y,line,size,key,color);y+=leading;line='' if ch=='\n' else ch
  else:line+=ch
 if line:tx(d,x,y,line,size,key,color);y+=leading
 return y

def card(n,title,h=1480,sub='第二版 / 可核验教学图解'):
 im=Image.new('RGB',(1120,h),BG);d=ImageDraw.Draw(im)
 tx(d,64,48,f'{n:02d}  /  {sub}',23,color=TEAL)
 size=47
 while d.textlength(title,font=ft('cn',size))>992:size-=1
 tx(d,64,104,title,size)
 d.line((64,190,1056,190),fill=INK,width=2)
 tx(d,64,h-57,'字的性格  /  真实字体排印 · 原创版面与结构示意',23,color=MUTED)
 return im,d

def panel(d,y,label,h):
 d.rounded_rectangle((64,y,1056,y+h),radius=18,fill=PAPER)
 tx(d,92,y+24,label,28,color=TEAL)
 return y+80

def save(im,name):
 im.save(OUT/name,optimize=True)

def fig31():
 im,d=card(31,'结构不同，部件也需要重新适配',1700)
 for i,(lab,words,desc) in enumerate([
  ('A  独体、左右、上下：观察真实字体中的空间','木  林  森','林中的木更窄；森的三个木还受上下位置影响。'),
  ('B  左右与上下：先辨认结构，再找留白','明  休  吕  昌','同一字号排印；观察整字留白，不是机械分割公式。'),
  ('C  包围结构：内部空间不是空着就行','回  国  园','留意外框、内件与底部的关系；并非每个内件等大。')]):
  yy=panel(d,225+i*440,lab,405)
  tx(d,106,yy+20,words,142,'song')
  wrap(d,100,yy+230,desc,890,29,color=MUTED)
 wrap(d,92,1570,'样张：Noto Sans SC Regular。比较的是整字轮廓；没有抽取或机械缩放源字体部件。',925,24,color=MUTED)
 save(im,'fig-31.png')

def fig32():
 im,d=card(32,'扩展图鉴：三个不同的观察维度',1660)
 samples=[('A  宽度：Nimbus Sans Narrow','NimbusSansNarrow-Regular.otf','HAMBURG 0123','窄体描述比例；不自动说明衬线、年代或用途。'),('B  衬线：C059 Roman','C059-Roman.otf','Hamburg 0123','观察较厚的衬线；这一款样张不代表所有板状衬线。'),('C  笔势：Z003 MediumItalic','Z003-MediumItalic.otf','Quiet morning','观察倾斜、连接和升降部；真实字体排印。')]
 for i,(lab,key,s,desc) in enumerate(samples):
  yy=panel(d,225+i*435,lab,400);tx(d,100,yy+30,s,92,key)
  wrap(d,100,yy+215,desc,900,29,color=MUTED)
 save(im,'fig-32.png')
 im,d=card(32,'圆润与模板字：结构方法对照',1510)
 yy=panel(d,225,'D  真实圆体样张：M PLUS Rounded 1c Regular',400)
 tx(d,100,yy+25,'清風讀書',145,'MPLUSRounded1c-Regular.ttf')
 wrap(d,100,yy+220,'日文字库中的汉字样张；用于观察圆润笔端，不是简体中文规范样本。',900,29,color=MUTED)
 yy=panel(d,660,'E  原创模板字 O：连接桥保留中间材料',650)
 for x,gap in [(150,False),(610,True)]:
  d.ellipse((x,yy+25,x+285,yy+310),fill=INK)
  d.ellipse((x+77,yy+102,x+208,yy+233),fill=PAPER)
  if gap:
   d.rectangle((x+125,yy+20,x+160,yy+315),fill=PAPER)
  tx(d,x,yy+355,'普通镂空' if not gap else '加入连接桥',30)
 wrap(d,100,yy+435,'桥位、宽度与数量须按材料和工艺另行设计；这是单字母几何示意，不是完整字库。',900,28,color=MUTED)
 save(im,'fig-32-extra.png')

def fig32history():
 im,d=card(32,'隶书来源：曹全碑拓本的真实影像',1700)
 yy=panel(d,225,'F  实物参照：上海博物馆所摄拓本',620)
 original=Image.open(OUT/'history-caoquan.jpg').convert('RGB')
 crop=original.crop((0,900,3648,2400));crop.thumbnail((920,410));im.paste(crop,(100,yy+10))
 wrap(d,100,yy+445,'照片保留观看角度；不要把拍摄透视当成字形本身的比例。',900,27,color=MUTED)
 yy=panel(d,885,'G  局部裁切：看横向展开与笔画收放',520)
 crop=original.crop((1750,1070,2650,2120));crop.thumbnail((360,370));im.paste(crop,(115,yy+15))
 wrap(d,540,yy+35,'从整页回到局部，观察横画、撇捺和字间节奏。\n\n这是历史拓本照片，不是当代数字隶书字体。',420,31)
 wrap(d,92,1450,'摄影 Shallowell，2020-08-20；CC BY-SA 4.0。本图做裁切、缩放与教学编排，整张图卡按同许可提供。',925,28,color=MUTED)
 wrap(d,92,1560,'来源：Wikimedia Commons / Caoquan Bei - 144020.jpg',925,22,color=MUTED)
 save(im,'fig-32-li.png')
 im,d=card(32,'小篆字头与释文：同页并存的不同字形',1750)
 yy=panel(d,225,'H  《说文解字》子部条目：真实书页影像',1120)
 original=Image.open(OUT/'history-shuowen-zi.png').convert('RGB');crop=original.copy();crop.thumbnail((350,1010));im.paste(crop,(110,yy+5))
 crop=original.crop((545,0,831,400));crop.thumbnail((310,300));im.paste(crop,(610,yy+15))
 tx(d,580,yy+350,'右上：小篆字头“子”',30,color=TEAL)
 wrap(d,560,yy+435,'左侧整条图像还保留古文、籀文与释文。这里比较的是历史字书中的不同字形角色。',450,32)
 wrap(d,560,yy+660,'只把特定字头当作篆形参照；不要把旁边的释文统称为篆体。',450,32,color=MUTED)
 wrap(d,92,1400,'来源：《说文解字》“子”条，四库全书荟要扫描本，第 78 页；Wikimedia Commons 文件 Shuowen-子.png。',925,28,color=MUTED)
 wrap(d,92,1540,'原件与影像标识为公有领域；本图只做裁切、缩放与教学编排，不是新造的数字篆体字体。',925,28,color=MUTED)
 save(im,'fig-32-seal.png')

def fig33():
 im,d=card(33,'换行、标点与竖排：逐项检查',1640)
 yy=panel(d,225,'A  手工错误换行示例：句号落到行首',340)
 tx(d,105,yy+15,'欢迎来到清风读书会',55,'song');tx(d,105,yy+100,'。一起读书，一起分享。',55,'song',RED)
 wrap(d,105,yy+207,'只为展示问题手动断行；不是浏览器实际排版测试。',880,27,color=MUTED)
 yy=panel(d,600,'B  调整行内容：把句末点号留在前一行',340)
 tx(d,105,yy+15,'欢迎来到清风读书会。',55,'song');tx(d,105,yy+100,'一起读书，一起分享。',55,'song')
 wrap(d,105,yy+207,'实际排版要同时核对禁则、行宽、字距和标点处理。',880,27,color=MUTED)
 yy=panel(d,975,'C  真实竖排：右列先读，再读左列',480)
 font=ft('song',59)
 for x,s in [(930,'清风读书会。'),(800,'一起读书。')]:
  d.text((x,yy+10),s,font=font,fill=INK,direction='ttb',features=['vert','vrt2'],anchor='rt')
 wrap(d,105,yy+35,'采用 Noto Sans SC，启用 vert / vrt2 竖排替换；观察句号位置。',540,32,color=MUTED)
 wrap(d,105,yy+220,'横排字体直接逐字旋转，不能替代竖排字形与排版规则。',540,32,color=MUTED)
 save(im,'fig-33.png')

def fig33extra():
 im,d=card(33,'标点占位：改的是空间，不是字形',1470)
 yy=panel(d,225,'D  连续标点：手工占位示意',600)
 for row,gap,lab in [(0,120,'全角占位'),(1,65,'压缩相邻空白')]:
  y=yy+25+row*200;x=155
  tx(d,x,y,lab,28,color=MUTED)
  for j,ch in enumerate('。」'):
   xx=x+340+j*gap
   d.rectangle((xx,y-5,xx+120,y+120),outline=LINE,width=2)
   tx(d,xx,y+110,ch,120,anchor='ls')
 wrap(d,100,yy+430,'两行字形大小不变，只调整前进位置；方框是原始全角占位参照，不是 CSS 自动渲染结果。',900,29,color=MUTED)
 yy=panel(d,860,'E  将组合整体检查：避免机械逐字拆行',400)
 tx(d,110,yy+30,'25 kg    ……    ——',75)
 wrap(d,100,yy+185,'数量与单位、成对省略号与破折号的断行处理，应按语言规范和实际排版环境分别核对。',900,29,color=MUTED)
 save(im,'fig-33-extra.png')

def fig34():
 im,d=card(34,'数字：高度与占位是两组独立选择',1720)
 for i,(lab,features,desc) in enumerate([
  ('A  齐线数字 / lnum + pnum',['lnum','pnum'],'顶端高度接近，数字仍可有不同的前进宽度。'),
  ('B  旧式数字 / onum + pnum',['onum','pnum'],'部分数字有升降变化；用于正文时观察整体节奏。'),
  ('C  等宽数字 / lnum + tnum',['lnum','tnum'],'同一列小数点对齐；先保证每行采用相同单位和位数。')]):
  yy=panel(d,225+i*440,lab,405)
  tx(d,102,yy+20,'0123456789',110,'source',features=features)
  if i==2:
   for j,s in enumerate(['  11.00','  88.88']): tx(d,110+410*j,yy+155,s,59,'source',features=features)
  wrap(d,100,yy+260,desc,890,28,color=MUTED)
 wrap(d,92,1580,'同一字体 Source Serif 4，字重 400 / 光学字号 20。通过真实 OpenType 特性切换；没有拉伸或手工重画数字。',925,25,color=MUTED)
 save(im,'fig-34.png')

def page(d,x,y,w,h,revised):
 d.rectangle((x,y,x+w,y+h),fill='white',outline=LINE,width=2)
 pad=52 if revised else 24
 tx(d,x+pad,y+50,'清风读书会',52 if revised else 42,'song')
 if revised:
  tx(d,x+pad,y+125,'把阅读带回日常',27,color=TEAL)
  d.line((x+pad,y+188,x+w-pad,y+188),fill=LINE,width=2)
  lines=['一张桌子，几本书，几位愿意分享的人。','读书会从一次短短的朗读开始。我们先说','出自己记住的句子，再谈它与生活的关系。','','本期主题：城市里的树','带一本与自然有关的书，也可以空手来。','活动提供公共读本，欢迎第一次参加。']
  for i,s in enumerate(lines):tx(d,x+pad,y+220+i*49,s,27,'song')
  d.rectangle((x+pad,y+620,x+w-pad,y+750),fill='#e4eeea')
  tx(d,x+pad+24,y+645,'带走一条观察线索',29,color=TEAL)
  tx(d,x+pad+24,y+703,'回家路上，试着认出一种街边树。',25)
  tx(d,x+pad,y+h-68,'清风读书会    /    活动读本                  1',23,color=MUTED)
 else:
  lines=['一张桌子，几本书，几位愿意分享的人。','读书会从一次短短的朗读开始。我们先说','出自己记住的句子，再谈它与生活的关系。','本期主题：城市里的树','带一本与自然有关的书，也可以空手来。','活动提供公共读本，欢迎第一次参加。','带走一条观察线索：','回家路上，试着认出一种街边树。']
  for i,s in enumerate(lines):tx(d,x+pad,y+130+i*39,s,27,'song')

def fig35():
 for label,rev,name in [('A  初稿：段落与提示混在同一层级',False,'fig-35.png'),('B  修订：先看主题，再读正文与实践提示',True,'fig-35-revised.png')]:
  im,d=card(35,'书籍案例：让页面组织阅读',1490)
  tx(d,84,228,label,30,color=TEAL);page(d,180,300,760,1000,rev)
  wrap(d,94,1330,'原创单页排版样件。图中展示组织关系；字号、行长与纸张尺寸仍需按实尺寸印样检查。',930,27,color=MUTED)
  save(im,name)

def fig35pages():
 data=[(2,'当天安排',[('时间表','14:00  开场介绍','14:15  个人分享','15:15  自由讨论','15:50  结束整理'),('分享时，请留出倾听的空间。','每人先读一段短文，再讲自己的观察。','主持人提示轮次，参与者可以选择跳过。')]),(3,'延伸阅读',[('读书会之后','带走一条问题，沿着它继续找书。','把自己的摘录和想法分开记录，','也记下书名、作者和页码。'),('下一次见面','欢迎带来沿途观察到的一棵树。','照片、叶片速写和一段文字都可以。')])]
 for num,title,groups in data:
  im,d=card(35,'连续读本：同一系统中的后续页面',1490)
  tx(d,84,228,f'C{num-1}  修订读本 / 第 {num} 页',30,color=TEAL)
  x=180;y=300;w=760;h=1000;pad=52
  d.rectangle((x,y,x+w,y+h),fill='white',outline=LINE,width=2)
  tx(d,x+pad,y+50,title,52)
  tx(d,x+pad,y+125,'清风读书会 / 城市里的树',27,color=TEAL)
  d.line((x+pad,y+188,x+w-pad,y+188),fill=LINE,width=2)
  yy=y+240
  for group in groups:
   tx(d,x+pad,yy,group[0],34,color=TEAL);yy+=75
   for line in group[1:]:tx(d,x+pad,yy,line,27);yy+=51
   yy+=60
  tx(d,x+pad,y+h-68,f'清风读书会    /    活动读本                  {num}',23,color=MUTED)
  wrap(d,94,1330,'与前页保持相同页边距、正文节奏和页码位置；时间表允许按内容分组，不强求各页长得一样。',930,27,color=MUTED)
  save(im,f'fig-35-page{num}.png')

def poster(d,x,y,w,h,rev):
 d.rectangle((x,y,x+w,y+h),fill='#e4eeea' if rev else '#fffdf8',outline=LINE,width=2)
 if rev:
  tx(d,x+50,y+50,'清风读书会 / 第一期',27,color=TEAL)
  tx(d,x+50,y+170,'城市里的树',78,'song')
  tx(d,x+50,y+300,'一起读书，一起分享',35)
  d.line((x+50,y+400,x+w-50,y+400),fill=TEAL,width=3)
  for i,s in enumerate(['11月14日 14:00—16:00','清风社区阅览室','免费参加 · 每场 20 人']):tx(d,x+50,y+450+i*80,s,34)
  d.rounded_rectangle((x+50,y+750,x+w-50,y+850),radius=12,fill=TEAL)
  tx(d,x+95,y+782,'提前报名，预留座位',32,color='white')
 else:
  for i,s in enumerate(['清风读书会','城市里的树','一起读书，一起分享','11月14日14:00—16:00','清风社区阅览室','免费参加 每场20人','提前报名预留座位']):tx(d,x+40,y+90+i*110,s,37 if i%2==0 else 35)

def fig36():
 for lab,rev,name in [('A  初稿：所有信息争夺同等注意力',False,'fig-36.png'),('B  修订：主题 → 时间地点 → 报名',True,'fig-36-revised.png')]:
  im,d=card(36,'海报案例：给目光一条清楚的路径',1480)
  tx(d,84,230,lab,30,color=TEAL);poster(d,180,300,760,1000,rev)
  wrap(d,94,1335,'原创虚构活动海报。保持核心文案一致，调整字号、分组与留白，再测试观看距离。',930,27,color=MUTED)
  save(im,name)

def fig37():
 im,d=card(37,'包装案例：纸套如何围住阅读模型',1660)
 yy=panel(d,225,'A  四面纸套：正面、侧面、背面与粘口',620)
 x=170;y=yy+70; widths=[245,125,245,125]; labs=['A 正面','B 侧面','C 背面','D 侧面'];xx=x
 d.rectangle((x-48,y,x,y+330),outline=TEAL,width=2)
 tx(d,x-42,y+120,'粘',24,color=MUTED);tx(d,x-42,y+162,'口',24,color=MUTED)
 for w,lab in zip(widths,labs):
  d.rectangle((xx,y,xx+w,y+330),fill='#e4eeea' if lab=='A 正面' else '#f5f1e9',outline=TEAL,width=2)
  tx(d,xx+12,y+18,lab,23,color=TEAL)
  if lab=='A 正面':
   tx(d,xx+20,y+95,'清风读书会',36);tx(d,xx+20,y+170,'茶间阅读',42)
  if lab=='B 侧面':
   for j,ch in enumerate('阅读时的一杯清茶'):tx(d,xx+46,y+75+j*26,ch,22)
  if lab=='C 背面':
   for j,line in enumerate(['冲泡提示：','按茶样另附说明','活动纪念纸套']):tx(d,xx+18,y+100+j*50,line,25)
  if xx!=x:d.line((xx,y,xx,y+330),fill=RED,width=3)
  xx+=w
 wrap(d,100,yy+470,'红线：折线。活动名完整留在正面，粘口不排字；本例为无顶底盖的纸套，不是盒子刀模。',900,29,color=MUTED)
 yy=panel(d,885,'B  围住模型：上下敞开，主面完整可读',530)
 x=350;y=yy+55
 d.polygon([(x,y),(x+285,y),(x+285,y+285),(x,y+285)],fill='#e4eeea',outline=TEAL,width=3)
 d.polygon([(x+285,y),(x+415,y-65),(x+415,y+220),(x+285,y+285)],fill='#cddfd8',outline=TEAL,width=3)
 d.polygon([(x,y),(x+130,y-65),(x+415,y-65),(x+285,y)],fill='#d9d7cf',outline=MUTED,width=2)
 tx(d,x+32,y+85,'清风读书会',43);tx(d,x+32,y+165,'茶间阅读',48)
 tx(d,110,yy+15,'灰色：被纸套围住的长方体阅读模型',27,color=MUTED)
 wrap(d,100,yy+365,'侧面内容应沿实际表面另做印样；纸套展开与模型均为教学示意，不承担食品标签或生产规格。',900,28,color=MUTED)
 save(im,'fig-37.png')

def phone(d,x,y,w,h,mode):
 d.rounded_rectangle((x,y,x+w,y+h),radius=38,fill='white',outline=INK,width=3)
 pad=43;size=38 if mode=='large' else 29
 tx(d,x+pad,y+48,'清风读书会报名',43)
 tx(d,x+pad,y+135,'姓名',size)
 d.rounded_rectangle((x+pad,y+195,x+w-pad,y+278),radius=10,outline=MUTED,width=2)
 tx(d,x+pad+18,y+219,'林青',size)
 tx(d,x+pad,y+330,'联系邮箱',size)
 d.rounded_rectangle((x+pad,y+390,x+w-pad,y+480),radius=10,outline=RED if mode=='error' else MUTED,width=2)
 tx(d,x+pad+18,y+417,'qingfeng@' if mode=='error' else 'qingfeng@example.org',size,'sans')
 if mode=='error':tx(d,x+pad,y+510,'请输入有效邮箱地址',size,color=RED)
 wrap(d,x+pad,y+585,'用于接收本次活动通知',w-2*pad,size,color=MUTED)
 bh=155 if mode=='large' else 98
 d.rounded_rectangle((x+pad,y+h-74-bh,x+w-pad,y+h-74),radius=12,fill=TEAL)
 if mode=='large':
  tx(d,x+pad+25,y+h-195,'确认报名并接收',size,color='white')
  tx(d,x+pad+25,y+h-135,'活动通知',size,color='white')
 else:tx(d,x+pad+50,y+h-138,'提交报名',size,color='white')

def fig38():
 for title,mode,name in [('A  常规状态：文字角色清楚','normal','fig-38.png'),('B  错误状态：说明问题并保留操作','error','fig-38-error.png'),('C  文字放大：重新留出空间','large','fig-38-large.png')]:
  im,d=card(38,'手机案例：文字要承受真实状态',1470)
  tx(d,84,230,title,30,color=TEAL);phone(d,200,300,720,970,mode)
  wrap(d,94,1320,'原创表单版面样件。放大图为重新排版示意；真实界面还需验证 200% 文字缩放、窄屏与键盘操作。',930,27,color=MUTED)
  save(im,name)

def fig39():
 im,d=card(39,'把原创网格字变成可输入的字体',1670)
 yy=panel(d,225,'A  H 的 5 × 7 网格：只把实心格写成轮廓',580)
 pattern=['10001','10001','10001','11111','10001','10001','10001'];u=53;x=190;y=yy+10
 for row,line in enumerate(pattern):
  for col,c in enumerate(line):d.rectangle((x+col*u,y+row*u,x+(col+1)*u-2,y+(row+1)*u-2),fill=INK if c=='1' else '#ecede8',outline=LINE)
 wrap(d,560,yy+35,'坐标：字高 700\n左右留白各 50\n前进宽度 600\n每 em 为 1000',390,33,color=MUTED)
 yy=panel(d,845,'B  实际 TTF 排印：HELLO / A LITTLE',500)
 tx(d,100,yy+5,'HELLO',115,'practice');tx(d,100,yy+160,'A LITTLE',115,'practice')
 wrap(d,100,yy+325,'PracticeGrid Atlas Regular：支持 AEHILOT 与空格。未覆盖字符可能回退或显示缺字框；不是完整英文字体。',900,28,color=MUTED)
 wrap(d,92,1420,'本书原创轮廓，随附构建脚本与 JSON 网格。修改网格 → 重新构建 → 安装或打开字体查看器 → 用覆盖字符测试。',925,30,color=MUTED)
 save(im,'fig-39.png')

def fig40():
 im,d=card(40,'可变字体：一次只改变一根轴',1650)
 for i,(label,axis,a,b,desc) in enumerate([
  ('A  字重轴 wght：宽度轴保持 100','wght',300,650,'笔画与空间共同变化；不是给原轮廓加粗描边。'),
  ('B  宽度轴 wdth：字重轴保持 400','wdth',75,125,'字形按设计轴变化；不是把位图机械横向拉伸。')]):
  yy=panel(d,225+i*605,label,570)
  for j,v in enumerate([a,b]):
   axes={'wght':v if axis=='wght' else 400,'wdth':v if axis=='wdth' else 100}
   tx(d,105,yy+15+j*145,'Reading type',94,'MozillaHeadline[wdth,wght].ttf',axes=axes)
   tx(d,105,yy+110+j*145,f'{axis} = {v}',24,'sans',MUTED)
  wrap(d,100,yy+370,desc,900,29,color=MUTED)
 wrap(d,92,1480,'真实字体：Mozilla Headline。wght 范围 200—700；wdth 范围 75—125。数值只对应这套字体。',925,28,color=MUTED)
 save(im,'fig-40.png')
 im,d=card(40,'光学字号：同样大小，不同轮廓',1510)
 for i,(val,desc) in enumerate([(8,'面向小尺寸的设计位置'),(60,'面向大尺寸的设计位置')]):
  yy=panel(d,225+i*445,f'{chr(65+i)}  Source Serif 4 / opsz = {val}',410)
  tx(d,105,yy+20,'Reading 2026',102,'source',axes={'wght':400,'opsz':val})
  tx(d,105,yy+180,'a e s  1 2 3',85,'source',axes={'wght':400,'opsz':val})
  tx(d,105,yy+280,desc,28,color=MUTED)
 wrap(d,92,1175,'两组字样都按相同像素字号排印，字重轴固定 400；只改变 opsz。比较笔画对比、细节和间距。',925,32)
 wrap(d,92,1330,'本字体 opsz 范围 8—60；它不是所有可变字体都具有的轴。实际小尺寸还应在目标设备上测试。',925,28,color=MUTED)
 save(im,'fig-40-opsz.png')

def main():
 for fn in [fig31,fig32,fig32history,fig33,fig33extra,fig34,fig35,fig35pages,fig36,fig37,fig38,fig39,fig40]:fn()
 print('Rendered',len(list(OUT.glob('fig-3[1-9]*.png')))+len(list(OUT.glob('fig-40*.png'))),'expansion cards')
 for name in USED:
  f=TTFont(F/name)
  # Specimen glyph coverage is validated in tx().
 print('Fonts:',sorted(USED))
def fetch_assets():
 import requests
 for row in json.loads((ROOT/'references/expansion-fonts.json').read_text()):
  dest=F/row['file']
  if not dest.exists():
   r=requests.get(row['source'],timeout=90);r.raise_for_status()
   if hashlib.sha256(r.content).hexdigest()!=row['sha256']:raise ValueError('Font source changed: '+row['file'])
   dest.write_bytes(r.content)
 print('Expansion fonts ready; licenses are bundled under assets/fonts/.')

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--fetch-assets',action='store_true',help='Download missing, checksum-verified expansion fonts before rendering')
 args=parser.parse_args()
 if args.fetch_assets:fetch_assets()
 main()

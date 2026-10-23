# 图片、字体与重建说明

本版样张使用真实字体文件，由 Pillow/FreeType 排印。结构、间距与排版图使用可复现绘图程序制作。没有把生成图片里的偶然文字当作字体样本。

## 图片的身份

- `fig-01.png` 至 `fig-30.png`：三十章主图，具体样张身份写在面板内。
- `fig-12-extra.png`：数字楷体、拉丁花体与本书原创模块字的补充对照。
- `fig-20-extra.png`：中西混排字号与基线候选参数的单变量比较。
- `fig-27-extra.png`：原创四字几何标题「日月山水」完整步骤；可编辑SVG随工程提供。
- `historical-kelmscott-title.png`、`historical-kelmscott-opening.png`：Smithsonian馆藏1896年Kelmscott Chaucer实物影像，仅分裁为单页；馆方标识public domain，来源详见`historical-image.json`。
- `cover.png`：本书原创封面，采用真实字体排印。

大部分样张采用同字样对照。第19章等用途示例明确改变了文案和任务，不能作为字体可读性实验。第24章的AV字标练习使用现成DejaVu字形配线条，没有声称原创了这两个字母的轮廓。第27章几何“日”字是原创局部设计练习，不是一套成品字体。

## 字体来源

| 用途 | 原始字体/家族 | 来源和许可记录 |
|---|---|---|
| 中文标签、黑体参照 | Noto Sans SC Regular | 环境已有的字体；已核对字体内名称和OFL声明，保留名称元数据与OFL |
| 宋体与地区字形 | Noto Serif CJK SC/TC/JP Regular | [Noto CJK官方项目](https://github.com/notofonts/noto-cjk)，OFL |
| 楷体与仿宋样张 | FandolKai Regular、FandolFang Regular | [CTAN Fandol](https://ctan.org/pkg/fandol)，随附COPYING记录；字体文件通过脚本另取 |
| 拉丁字形、字重、字偶 | DejaVu Sans/Serif/Sans Mono | [DejaVu项目](https://dejavu-fonts.github.io/)，随附原许可 |
| 拉丁衬线、无衬线、窄体与花体参照 | Nimbus Roman、P052、C059、Nimbus Sans、Nimbus Sans Narrow、URW Gothic、Z003 | [URW Base35官方项目](https://github.com/ArtifexSoftware/urw-base35-fonts)，保留其许可记录；字体文件通过脚本另取 |

所有字体的许可各自适用，书稿的存在不改变字体本身的权利。图像中的点阵字样与字体文件是不同交付物。品牌字体补充资料见第26章与`sources-c.md`；对应字体文件的许可与来源记录随素材保留。

## 控制文件大小

工程中的Noto Serif教学字体只保留本版样张和文字需要的字符，内部家族名改为`BookSpecimen…`，以免与完整字体混淆。图片面板标的是原始字形设计来源。子集没有重新设计字形；它也不适合安装后当作通用字库。Noto Sans SC保留原文件；三款宋体原始文件的名称、版本和摘要保存在`font-subsets.json`。

工程内已保留成品图片，重建EPUB不需要安装字体或联网。只有重新绘图时才需要额外字体，运行`python scripts/fetch_fonts.py`后再运行两个绘图脚本。后续加入新文字时，要先检查子集覆盖；必要时从官方项目取得完整字体，再用可选脚本重新制作教学子集。

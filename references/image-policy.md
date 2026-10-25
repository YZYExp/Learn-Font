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


## 扩充版新增图稿与实践附件

第31–40章共新增21张正文教学图（主图及补图），分别演示结构、风格、中文精排、数字特性、四媒介案例、实际小字库与可变轴。图35包含单页初稿、修订以及后续两页；图38分别展开正常、错误和大字状态。全部通过真实字体排印或可校验结构绘制，不用生成图中文字作为字体证据。

- `fig-32-li.png`：Shallowell 摄《曹全碑》拓本照片的裁切、缩放与教学编排；原图和整张衍生图卡适用 **CC BY-SA 4.0**。作者、来源、变更与许可记录见 `expansion-image-sources.json` 及第32章，不将它并入其他原创资产许可。
- `fig-32-seal.png`：《说文解字》“子”条公有领域扫描影像及局部放大，明确区分小篆字头、古文、籀文与释文；不作为现代数字篆体字体样张。
- M PLUS Rounded 1c 为日文字库，本书仅用其汉字观察圆润笔端，不能代表简体中文规范。Source Serif 4 用于真实数字特性与光学字号比较。两者来源、原文件摘要、OFL许可路径见 `expansion-fonts.json`。
- 现有 Mozilla Headline 原文件也用于网站字体实验台；网站保留其OFL文件。实验台显示该版本实际提供的 `wght` 与 `wdth`，没有虚构 `opsz`。
- `PracticeGrid Atlas` 是本书原创七字母练习字体，包含空格及 A/E/H/I/L/O/T，未使用现成字体轮廓，原创网格与TTF按CC0提供，详见 `assets/designs/practice-font-README.md`。该许可仅针对这份练习资产。

新增图稿采用 `scripts/make_expansion_figures.py` 重建；缺字体时使用 `--fetch-assets`。既有URW样张字体仍由 `scripts/fetch_fonts.py` 下载；七字母练习由 `scripts/build_practice_font.py` 重建。网站与EPUB直接使用成品PNG，不下载或重跑制图。

EPUB含原始实践附件及对应XHTML说明页；字体和JSON需要解包提取或从在线版下载，不假定每个阅读器能直接安装字体。网页保留直接文件链接。

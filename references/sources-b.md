# 第11–20章资料核验记录

核验日期：2026-10-22。正文以具体链接就近引用，以下为资料与适用边界。教学例子、观察练习和组合判断为本书原创说明，不伪称资料中的实验结论。

| 资料 | 用途 | 边界 |
|---|---|---|
| [DejaVu Fonts](https://dejavu-fonts.github.io/) | 11章真实字体项目身份 | 不据项目名称推导所有字形细节；字样以实际文件为准 |
| [Artifex URW Base35](https://github.com/ArtifexSoftware/urw-base35-fonts) | 11章 Nimbus／URW 字体来源 | 不把不同家族当作同一家族变体 |
| [Google Design：How to Choose a Web Font](https://design.google/library/choosing-web-fonts-beginners-guide) | 11章实际阅读条件 | 不泛化无衬线一定比衬线易读 |
| [OpenType hmtx](https://learn.microsoft.com/en-us/typography/opentype/spec/hmtx) | 12、15、17章前进宽度与边距 | 数值度量不等于可见轮廓宽度 |
| [OpenType GSUB](https://learn.microsoft.com/en-us/typography/opentype/spec/gsub) | 12章替代字形与上下文替换 | 功能必须有字体数据与应用支持 |
| [Unicode Chinese and Japanese FAQ](https://www.unicode.org/faq/han_cjk.html) | 13章编码与地区字形 | 未把地区差异写成简繁转换 |
| [Adobe Source Han Sans](https://github.com/adobe-fonts/source-han-sans) | 13章地区版本 | 字体配置与软件语言标记都需检查 |
| [Noto CJK](https://github.com/notofonts/noto-cjk) | 13章 SC／TC(TW)／JP 真实样张来源 | 比较限定「骨、直、令、返」，不含香港或韩国版本 |
| [Adobe Source Han Sans goes variable](https://blog.adobe.com/en/publish/2021/04/08/source-han-sans-goes-variable) | 13、18章多地区与可变字体案例 | 不声称此后发行状态或最新版本 |
| [W3C Language enablement index](https://www.w3.org/TR/typography/) | 13章不同文字系统的排版需求 | 不把各文字系统混成同一规则 |
| [W3C 中文排版需求](https://www.w3.org/TR/clreq/) | 13、20章延伸阅读 | 当前为 Group Note Draft／工作材料，非普遍强制标准；只作为工作文档引用 |
| [FontForge Font and glyph creation](https://fontforge.org/docs/tutorial/editexample.html) | 14章轮廓编辑机制 | 骨架是本书观察方法，不伪称所有字体内部必有骨架 |
| [FontForge Expand Stroke](https://fontforge.org/docs/techref/stroke.html) | 14章轮廓扩展辅助 | 加描边不等于完成粗体设计 |
| [FontForge Typographical glossary](https://fontforge.org/docs/glossary.html) | 15、16章 x高、升降部、越界 | 中宫不伪造通用比例；overshoot无统一固定值 |
| [FontForge Bézier Splines](https://fontforge.org/docs/techref/bezier.html) | 16章曲线表示 | 未把所有曲线格式都称为三次贝塞尔 |
| [FontForge Outline Glyph View](https://fontforge.org/docs/ui/mainviews/charview.html) | 16章节点与工具检查 | 工具校验不等于审美正确 |
| [FontForge Metrics, spacing and kerning](https://fontforge.org/docs/tutorial/editexample5.html) | 17章边距与组合测试 | 不采用其中带有历史平台局限的行距概述作为当前实现结论 |
| [OpenType GPOS](https://learn.microsoft.com/en-us/typography/opentype/spec/gpos) | 17章定位与字偶调整 | 图若人工调距需明标，不冒充字体内建kerning |
| [OpenType Axis Registry](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg) | 18章可变轴机制 | 不以变化轴自动生成设计的说法替代设计工作 |
| [OpenType opsz](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_opsz) | 19章光学尺寸 | 与字号、设备尺寸、观看距离区分 |
| [WAI Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | 19章网页文字对比 | 明确网页适用范围，正文未套用数值到印刷或导视 |
| [WAI Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) | 19章文字放大与可用性 | 非一般美学准则 |
| [OpenType BASE](https://learn.microsoft.com/en-us/typography/opentype/spec/base) | 20章不同文字基线关系 | 机制存在不代表所有应用自动完成协调 |
| [Adobe Source Han Sans introduction](https://blog.adobe.com/en/publish/2014/07/15/introducing-source-han-sans-an-open-source-pan-cjk-typeface) | 20章多文字家族案例 | 不推导所有中文字体都应搭 Source Sans |

## 图文整合要求

- 11：DejaVu Sans／Nimbus Sans／URW Gothic 真实字样。
- 12：主图等宽／比例只演示占位；补图使用FandolKai真实数字楷体、Z003 MediumItalic真实花体、原创矩形模块TYPE四字，不把字体排印伪称手迹。
- 13：Noto Serif CJK SC／TC(TW)／JP 的「骨、直、令、返」真实同码位地区字形比较；不含HK和KR，不能假设每字每版都有不同。
- 14：原创几何A的中心路径、等宽笔画与轮廓示意，非字体源稿。
- 15：上方国／心空间对照，下方同一国字缩放位置实验，非成熟字库的设计方案。
- 16：几何越界放大示意，无通用制作参数。
- 17：DejaVu Serif 135px，「AVATAR To」，Pillow RAQM关闭／开启字体自带kerning；正文已与实际图一致。
- 18：DejaVu Sans常规／粗体，Nimbus Sans Narrow为另一家族宽度参照；图中无斜体。
- 19：导视、书页、界面不同文案的用途示例，不是同文控制变量实验，不充当所有设备与距离的字号标准。
- 20：主图中文宋黑与拉丁组合为原创搭配实验；补图Noto Sans SC60px固定，DejaVu Serif由60px增至72px，再上移6px，明确为候选参数、不充当通用配方。

补图生成器：`scripts/make_extra_figures.py`，输出 `fig-12-extra.png` 与 `fig-20-extra.png`。Z003文件来自随系统安装的URW Base35字体，复制到工程以供可复现排印，沿用 `assets/fonts/LICENSE-URW.txt`；Fandol来源为 [CTAN项目页](https://ctan.org/pkg/fandol)。

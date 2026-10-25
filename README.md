# 字的性格

字体、字形设计与文字排版图解。扩充版含八篇四十章。面向有兴趣的非专业读者，沿着“看见差异 → 理解来历 → 拆解结构 → 学会选择与组合 → 亲手设计”阅读。

中文Markdown是唯一主稿。所有图片使用相对路径，目录与后续阅读站导航以`book.json`为准。阅读站源码位于`site/`，从同一份章节清单生成完整目录与导航。

## 阅读顺序

先读[阅读导引](appendices/00-guide.md)。

### 第一篇：先学会看字

- [1. 字为什么有不同的性格](chapters/01.md)
- [2. 字体、字形、书法、手写字与标志字](chapters/02.md)
- [3. 观察字的工具](chapters/03.md)

### 第二篇：字是怎样走到今天的

- [4. 汉字书写、刻印与印刷字的演变](chapters/04.md)
- [5. 拉丁字母与印刷字体的发展](chapters/05.md)
- [6. 从金属活字到数字屏幕](chapters/06.md)

### 第三篇：字体风格图鉴

- [7. 宋体与明朝体](chapters/07.md)
- [8. 黑体及其不同面貌](chapters/08.md)
- [9. 楷体、仿宋与书写风格](chapters/09.md)
- [10. 拉丁衬线体](chapters/10.md)
- [11. 拉丁无衬线体](chapters/11.md)
- [12. 等宽、手写、装饰与实验字体](chapters/12.md)
- [13. 中日韩字形、多文字系统与混排](chapters/13.md)

### 第四篇：字形是怎样设计出来的

- [14. 骨架、笔画与轮廓](chapters/14.md)
- [15. 字面、中宫、重心与视觉大小](chapters/15.md)
- [16. 曲线、转角和视觉修正](chapters/16.md)
- [17. 字距、字偶间距与连续阅读节奏](chapters/17.md)
- [18. 从几个字到一套字](chapters/18.md)

### 第五篇：怎样用好字体

- [19. 根据内容、媒介和阅读距离选字](chapters/19.md)
- [20. 中文与西文字体怎样搭配](chapters/20.md)
- [21. 字号、行距、行长与段落](chapters/21.md)
- [22. 标题、正文、注释和信息层级](chapters/22.md)
- [23. 书籍、海报、包装与屏幕界面的排版](chapters/23.md)

### 第六篇：字体在真实世界里

- [24. 品牌字体与定制字体](chapters/24.md)
- [25. 标志字、招牌与环境导视](chapters/25.md)
- [26. 当代品牌、出版物与数字产品案例](chapters/26.md)

### 第七篇：亲手做一次

- [27. 设计一组标题字](chapters/27.md)
- [28. 从草图、矢量轮廓到测试与修订](chapters/28.md)
- [29. 制作一张字体样张与一个应用页面](chapters/29.md)
- [30. 数字字体入门](chapters/30.md)

### 第八篇：从细节到完整作品

- [31. 中文结构与部件适配](chapters/31.md)
- [32. 扩展字体图鉴：圆、窄、板状衬线与模板字](chapters/32.md)
- [33. 中文精细排版：标点、换行与竖排](chapters/33.md)
- [34. 数字与符号：文字系统里容易忽略的一半](chapters/34.md)
- [35. 连续书页：把清风读书会做成一本小册](chapters/35.md)
- [36. 海报：从平均用力到清楚邀请](chapters/36.md)
- [37. 包装：文字必须跟着折线回到立体](chapters/37.md)
- [38. 手机报名页：文字要在变化中继续工作](chapters/38.md)
- [39. 做一个能输入的七字母练习字体](chapters/39.md)
- [40. 可变字体与屏幕上的真实阅读](chapters/40.md)

## 附录与素材

- [术语回查](appendices/01-glossary.md)
- [可以做完的小项目](appendices/02-workbook.md)
- [图片身份、字体来源与许可说明](references/image-policy.md)
- `assets/designs/riyueshanshui.svg`：可编辑原创四字几何练习
- `references/sources-a1.md`、`sources-a2.md`、`sources-b.md`、`sources-c.md`：分组资料核查记录；具体引用也保留在各章。

## 构建

从工程根目录运行。已有图片可直接用于EPUB，首次构建无需下载字体。

```bash
python -m pip install 'Markdown>=3.5,<4'
python scripts/build_epub.py
```

输出：`build/字的性格.epub`。脚本同时核查包内XML、图片、目录与本地链接。正文和图片可独立复用，整书导出与未来网页发布没有依赖绑定。

需要重新绘图或执行完整检查时，安装`requirements.txt`中的依赖，然后运行：

```bash
python -m pip install -r requirements.txt
python scripts/fetch_fonts.py
python scripts/make_figures.py
python scripts/make_extra_figures.py
python scripts/make_worked_title.py
python scripts/check_book.py
python scripts/build_epub.py
```

绘图用到的部分字体由`fetch_fonts.py`从官方项目或CTAN另取，许可记录已保留。随工程提供的Noto Serif为重命名教学子集，Noto Sans保留原文件，足以重建本版图像；增加新文字前须重新检查覆盖。

## 版本管理

首次提交仅含零字节`README.md`，后续按目录、正文、图像与审稿进展叠加提交。工程包中的`history.bundle`保留Git历史，可在另一个空目录恢复仓库：

```bash
git clone history.bundle font-atlas-restored
```

远端仓库：[YZYExp/Learn-Font](https://github.com/YZYExp/Learn-Font)。

## 在线阅读与发布

阅读站：[字的性格](https://yzyexp.github.io/Learn-Font/)。源码与阅读站共享同一份Markdown、图片与章节清单。

```bash
python -m pip install -r requirements-site.txt
python scripts/build_site.py --base-path /Learn-Font/ --output build/site --epub downloads/font-atlas.epub
python scripts/check_site.py --base-path /Learn-Font/ --output build/site
```

`pages.yml`只安装Markdown，完成网页和内部链接校验后部署；`export.yml`独立导出EPUB并保存30天Actions产物。两个流程互不依赖，PR只验证而不发布。

已核验的首版EPUB快照位于`downloads/font-atlas.epub`。`edition.json`记录内容摘要及文件摘要；当正文或图片更新而快照未更新时，网页自动改为导出入口，避免把旧包标为当前版本。Actions产物下载需要GitHub登录，并受30天保留期限制。

更新离线快照时，重新导出并验证EPUB，再更新摘要：

```bash
python scripts/build_epub.py
python -c "from pathlib import Path; import shutil; shutil.copy2(next(Path('build').glob('*.epub')), 'downloads/font-atlas.epub')"
python scripts/update_edition.py
```

Pages设置使用GitHub Actions作为发布来源。


## 扩充版实践资源

- 第31–34章：中文结构、扩展图鉴、中文精排、数字符号的真实字体对照。
- 第35–38章：同一虚构读书活动的书册、海报、包装与手机界面，保留初稿、修订和验收依据。
- 第39章：原创七字母练习字体 `assets/designs/practice-font-Regular.ttf`，可编辑源 `practice-font-grid.json`。重建：`python scripts/build_practice_font.py`。
- 第40章：可变轴、光学字号、回退与屏幕阅读。阅读站提供[字体实验台](https://yzyexp.github.io/Learn-Font/type-lab/)，随扩充版合并后发布。
- 新增图稿重建：`python scripts/make_expansion_figures.py --fetch-assets`。该命令下载缺失的新增字体并核对摘要；其字体来源、摘要和历史图片许可见 `references/expansion-fonts.json`、`references/expansion-image-sources.json` 与图片说明；已有PNG直接用于阅读和导出，不要求网页安装绘图依赖。

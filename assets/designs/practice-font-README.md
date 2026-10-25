# PracticeGrid Atlas：原创七字母练习字体

源：`practice-font-grid.json`。输出：`../fonts/PracticeGridAtlas-Regular.ttf`。
供阅读站下载的同内容副本为 `practice-font-Regular.ttf`。
从项目根目录执行 `python scripts/build_practice_font.py`；需要 fontTools。
轮廓是本项目原创的 5×7 模块并集，不取用任何现成字体轮廓。

覆盖：空格 U+0020，以及 A、E、H、I、L、O、T；另有未编码的 `.notdef`。
可以输入 `HELLO`、`A LITTLE`；其他字符不在范围内。
这是静态、单字重、等宽拉丁大写练习字体，未设置字偶调整或连字。
缺字时部分软件会使用后备字体，不能仅凭屏幕看起来有字就确认覆盖。

每个模块边长100字体单位，1000 units/em；大写顶700，基线0。
普通字前进宽600、左侧距50，空格前进宽300；行度量上800、下-200。
构建器会合并相邻方格的公共边，检查编码、度量、轮廓边界和测试文案。
修改网格只能使用5列7行的0/1，避免仅在角点相触的模块；修改后重新构建。
如修改字宽等工程参数，也须同步更新构建器校验和书中说明。

安装时使用独立字体族 `PracticeGrid Atlas`。可以先在字体预览器看样张，
无须替换系统字体。修订后另改字体族与PostScript名称，避免缓存混淆。

本目录中的原创网格数据、生成轮廓和该练习字体以 CC0 1.0 Universal 提供：
https://creativecommons.org/publicdomain/zero/1.0/ 。
此声明仅涉及这份原创练习资产，不改变工程内其他字体、图片及正文的许可。

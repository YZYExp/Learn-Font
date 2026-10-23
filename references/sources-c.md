# 21–30章资料与素材记录

核查日期：2026-10-22。以下为原始来源，正文分别就近引用。事实性概括与本书原创分析、练习建议分开表述。

| 章节 | 资料 | 用途与边界 |
|---|---|---|
|21|https://www.w3.org/WAI/WCAG22/Understanding/text-spacing|用户覆盖间距后的适应性，不误写为默认行高要求|
|21、23|https://www.w3.org/TR/clreq/|中文禁则、行与段落；当前为Group Note Draft，不称强制标准|
|22|https://design-system.service.gov.uk/styles/headings/|标题语义与样式分离|
|22|https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html|普通文字4.5:1、大字3:1及适用条件|
|23、29|https://design-system.service.gov.uk/styles/type-scale/|界面文字尺度系统|
|24、26|https://www.monotype.com/resources/duolingo-custom-font-inspired-their-owl-mascot-duo|原始项目记录，Feather由吉祥物形态发展；不声称当前全部界面均用此字|
|24、26|https://www.ibm.com/design/impact/plex/|Plex推出时间、家族和品牌背景|
|25|https://otc-cta.gc.ca/eng/publication/removing-communication-barriers-travellers-with-disabilities-code-practice|观看距离、字高、对比、反光等相互影响；不把本地条件普遍化|
|25|https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1044542/inclusive-mobility-a-guide-to-best-practice-on-access-to-pedestrian-and-transport-infrastructure.pdf|2021版公共交通无障碍实践背景，无直接抄写数值|
|26、29|https://protocol.mozilla.org/docs/fundamentals/typography|当前文字角色、uniwidth和字号尺度；不复制文档中可能有误的Sass示例|
|26|https://blog.mozilla.org/en/mozilla/mozilla-brand-next-era-of-tech/|2024品牌更新背景|
|26|https://design.theguardian.com/|标题、正文、栏目提示的角色，Titlepiece与logotype联系；页面搜索索引可读，open正文未返回|
|27、28|https://glyphsapp.com/learn/drawing-good-paths|曲线路径、节点、控制柄、极值等概念；练习过程为本书原创|
|28|https://fontforge.org/docs/tutorial/editexample.html|字体编辑器创建字形与参考线|
|30|https://learn.microsoft.com/en-us/typography/opentype/spec/cmap|字符编码与字形索引映射|
|30|https://learn.microsoft.com/en-us/typography/opentype/spec/otff|字体文件的表和轮廓表示|
|30|https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview|可变字体与设计轴|
|30|https://openfontlicense.org/|OFL用途、分发、修改和保留名称概述|

## 字体素材

Mozilla官方源仓库无编译ttf文件，本项目使用Google Fonts官方分发仓库同名字体，其OFL版权行指向Mozilla源项目。原始可变字体不改名、不修改；渲染时选择字重400，Headline宽度100。字形文件的内部legacy family name含ExtraLight是可变字体默认字重200所致，不能据此误标渲染实例。

- Mozilla Text：https://github.com/mozilla/mozilla-text-type
- Mozilla Headline：https://github.com/mozilla/mozilla-headline-type
- TTF与许可分发：https://github.com/google/fonts/tree/main/ofl/mozillatext 、https://github.com/google/fonts/tree/main/ofl/mozillaheadline
- IBM Plex Sans：https://github.com/IBM/plex ，文件位于packages/plex-sans/fonts/complete/ttf/IBMPlexSans-Regular.ttf，许可取根LICENSE.txt。保留Plex名称声明，未修改字形文件。

| 文件 | SHA-256 |
|---|---|
|MozillaText[wght].ttf|a74b1a5c77811bab140c8c30b02adea4f6a90fe8811c669c52541dd78f5c5e87|
|MozillaHeadline[wdth,wght].ttf|7d04f994cbffedacf9281f7d141c2d50bc7e3c02321bd8a12f7b323d813c7bdc|
|IBMPlexSans-Regular.ttf|975dcda37d80f038dcd143c22e33ca2d97a0cc5a929aace1c749153b0fe1afa5|
|mozillatext-OFL.txt|7796681a32b924d2dc5186e514bd53848dd72359f8f3f413797107a478ef1940|
|mozillaheadline-OFL.txt|d0f4ab49be920e6c7b99a1b51d7f35aa85a38afdd4a22db9fd4b4dab2390d178|
|IBMPlex-OFL.txt|7e6b2818edbd8f6a01ae80641cc8f16a51080d08fb4e532be3a0b6f74adb07da|

## 已知边界

- 不取得或分发Feather、Guardian字体，不用相似字体冒充真实样张；正文通过原项目链接观察。
- Duolingo旧Typography品牌规范已重定向设计博客，未用过时规范作当前用字依据。
- 包装章节的标签示例仅教学信息组织，不是行业法规清单；导视模拟不代替实地样件测试。
- 27章为固定四字标题项目，配原创几何「日」字局部练习与「日月山水」四字完整示范；不宣称已完成全字符字体。
- 所有练习的尺寸、数量限制都标明为实验起点，不作通用最佳实践承诺。

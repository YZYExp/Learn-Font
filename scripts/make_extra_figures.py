"""Additional, labelled specimens and controlled mixed-script experiments."""
from PIL import ImageDraw
from make_figures import base, panel, text, wrap, specimen, font, fonts, OUT, INK, TEAL, RED, MUTED

fonts['script'] = 'Z003-MediumItalic.otf'


def modular_word(draw, word, x, y, unit=23, gap=29):
    """Original seven-row bitmap letters; not extracted from any font."""
    forms = {
        'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
        'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
        'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
        'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
    }
    for char in word:
        for row, pattern in enumerate(forms[char]):
            for col, filled in enumerate(pattern):
                if filled == '1':
                    xx, yy = x + col * unit, y + row * unit
                    draw.rectangle((xx, yy, xx + unit - 1, yy + unit - 1), fill=INK)
        x += 5 * unit + gap


def extra12():
    im, d = base(12, '书写、花体与模块实验', 'ADDITIONAL SPECIMENS')
    y = panel(d, 246, 'A  FandolKai Regular / 书写特征参照', 310)
    specimen(d, '清风入林 山水有声', y + 5, 'kai', 91)
    text(d, (98, y + 166), '真实字体排印；不是手写原作，也不是书法手迹。', 27, 'cn', MUTED)
    y = panel(d, 596, 'B  Z003 MediumItalic / 拉丁书写式花体', 310)
    specimen(d, 'Quiet morning', y + 2, 'script', 135)
    text(d, (98, y + 166), '观察连接、倾斜与升降部；URW Base35 字体。', 27, 'cn', MUTED)
    y = panel(d, 946, 'C  原创模块字 TYPE / 几何矩形拼接', 370)
    modular_word(d, 'TYPE', 112, y + 4)
    wrap(d, (98, y + 198), '仅四个实验字母，不是完整字体；同一模块规则也要逐字检验可识读性。', 900, 27, 'cn', MUTED)
    im.save(OUT / 'fig-12-extra.png', optimize=True)


def mixed_sample(draw, baseline, english_size, shift=0):
    x = 108
    cn = '清风'
    draw.line((98, baseline, 1008, baseline), fill=TEAL, width=2)
    draw.text((x, baseline), cn, font=font('cn', 60), fill=INK, anchor='ls')
    x += draw.textlength(cn, font=font('cn', 60)) + 30
    draw.text((x, baseline - shift), 'Books 2026', font=font('serif', english_size), fill=INK, anchor='ls')
    if shift:
        draw.line((x - 8, baseline - shift, 1008, baseline - shift), fill=RED, width=2)


def extra20():
    im, d = base(20, '中西大小与位置：一次只改一个变量', 'CONTROLLED EXPERIMENT')
    settings = [
        ('A  相同字号：中文 60px / 拉丁 60px', 60, 0,
         '中文与拉丁共用基线；同字号不保证视觉大小相同。'),
        ('B  只改英文字号：60px → 72px', 72, 0,
         '中文仍为 60px；字号增加，英文基线保持不变。'),
        ('C  在 B 基础上：英文上移 6px', 72, 6,
         '红线为英文新基线；这是位置候选，不是通用配方。'),
    ]
    for i, (label, size, shift, explanation) in enumerate(settings):
        y = panel(d, 246 + i * 350, label, 310)
        mixed_sample(d, y + 84, size, shift)
        wrap(d, (98, y + 155), explanation, 900, 27, 'cn', MUTED)
    text(d, (98, 1320), 'Noto Sans SC + DejaVu Serif；数值对应本图原始排印。', 26, 'cn', MUTED)
    im.save(OUT / 'fig-20-extra.png', optimize=True)


if __name__ == '__main__':
    extra12()
    extra20()
    print('Rendered fig-12-extra.png and fig-20-extra.png')

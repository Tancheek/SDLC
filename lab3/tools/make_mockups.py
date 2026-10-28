"""Генератор PNG-мокапов для лабораторной работы №3 (SVS-RVC).

Запуск:  python lab3/tools/make_mockups.py
Результат: lab3/mockups/{main-window,render-dialog,live-monitor,model-manager}.png
"""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000
OUT = Path(__file__).resolve().parents[1] / "mockups"

# --- палитра ---------------------------------------------------------------
BG = "#0a0c11"
WIN = "#12151d"
PANEL = "#181c26"
PANEL_2 = "#202533"
PANEL_3 = "#272d3d"
BORDER = "#2b3243"
TEXT = "#e9edf6"
MUTED = "#8b95a9"
DIM = "#5f6a7e"
ACCENT = "#8b5cf6"
ACCENT_DARK = "#6d43e0"
ACCENT_SOFT = "#2a2340"
CYAN = "#22d3ee"
GREEN = "#34d399"
GREEN_SOFT = "#16352c"
AMBER = "#fbbf24"
AMBER_SOFT = "#3a2f12"
RED = "#f87171"
RED_SOFT = "#3a1c22"

FONT_DIR = Path(r"C:\Windows\Fonts")
REG = FONT_DIR / "segoeui.ttf"
BOLD = FONT_DIR / "segoeuib.ttf"
SEMI = FONT_DIR / "seguisb.ttf"

_fonts: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key not in _fonts:
        path = BOLD if bold else REG
        try:
            _fonts[key] = ImageFont.truetype(str(path), size)
        except OSError:
            _fonts[key] = ImageFont.load_default(size)
    return _fonts[key]


def text(d, xy, s, size=12, color=TEXT, bold=False, anchor="la"):
    d.text(xy, s, font=font(size, bold), fill=color, anchor=anchor)


def wrap(d, xy, s, width, size=12, color=TEXT, bold=False, leading=1.35):
    """Простой перенос по словам (для абзацев в мокапах не используется)."""
    words, line, x, y = s.split(), "", xy[0], xy[1]
    for word in words:
        probe = (line + " " + word).strip()
        if d.textlength(probe, font=font(size, bold)) <= width:
            line = probe
        else:
            text(d, (x, y), line, size, color, bold)
            y += int(size * leading)
            line = word
    if line:
        text(d, (x, y), line, size, color, bold)
    return y


def rr(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def hline(d, x1, x2, y, color=BORDER):
    d.line((x1, y, x2, y), fill=color, width=1)


def vline(d, x, y1, y2, color=BORDER):
    d.line((x, y1, x, y2), fill=color, width=1)


def dot(d, cx, cy, r, color):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)


def chip(d, x, y, label, fg=TEXT, bg=PANEL_3, size=9, pad_x=9, height=20, bold=False):
    w = int(d.textlength(label, font=font(size, bold))) + pad_x * 2
    rr(d, (x, y, x + w, y + height), height // 2, fill=bg)
    text(d, (x + w / 2, y + height / 2 + 1), label, size, fg, bold, anchor="mm")
    return w


def pill(dot_color, label, x, y, d, fg=GREEN, bg=GREEN_SOFT):
    w = int(d.textlength(label, font=font(9))) + 30
    rr(d, (x, y, x + w, y + 20), 10, fill=bg)
    dot(d, x + 11, y + 10, 3, dot_color)
    text(d, (x + 19, y + 10), label, 9, fg, anchor="lm")
    return w


def switch(d, x, y, on=True, width=34, height=18):
    bg = ACCENT if on else "#3a4152"
    rr(d, (x, y, x + width, y + height), height // 2, fill=bg)
    kx = x + width - height // 2 - 2 if on else x + height // 2 + 2
    dot(d, kx, y + height // 2, height // 2 - 3, "#ffffff")


def slider(d, x, y, width, value, label, value_text, accent=ACCENT):
    text(d, (x, y), label, 11, MUTED)
    text(d, (x + width, y), value_text, 11, TEXT, bold=True, anchor="ra")
    ty = y + 24
    rr(d, (x, ty, x + width, ty + 4), 2, fill="#2f3648")
    rr(d, (x, ty, x + int(width * value), ty + 4), 2, fill=accent)
    dot(d, x + int(width * value), ty + 2, 6, "#ffffff")


def base_window(title: str, subtitle: str, menu: bool = True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # мягкая «тень» окна
    rr(d, (30, 14, 1570, 986), 28, fill="#080a0e")
    rr(d, (36, 20, 1564, 980), 24, fill=WIN, outline=BORDER)
    # заголовок окна
    rr(d, (58, 36, 98, 76), 12, fill=ACCENT)
    for i, h in enumerate((10, 18, 26, 16, 8)):
        bx = 64 + i * 6
        d.rounded_rectangle((bx, 56 - h // 2, bx + 3, 56 + h // 2), 2, fill="#ffffff")
    text(d, (112, 38), title, 16, TEXT, bold=True)
    text(d, (112, 59), subtitle, 10, MUTED)
    # правые чипы
    x = 1516
    online_label = "Офлайн"
    online_w = int(d.textlength(online_label, font=font(9))) + 36
    rr(d, (x - 74, 44, x - 74 + online_w, 64), 10, fill="#16352c")
    dot(d, x - 74 + 11, 54, 3, GREEN)
    text(d, (x - 74 + 20, 54), online_label, 9, GREEN, anchor="lm")
    chip(d, x - 74 - online_w - 8, 44, "v0.2.0", MUTED, PANEL_2, 9, 9, 20)
    # меню
    if menu:
        y = 92
        hline(d, 40, 1560, y, BORDER)
        for i, item in enumerate(("Файл", "Правка", "Вид", "Рендер", "Справка")):
            text(d, (62 + i * 72, y + 15), item, 10, MUTED)
        text(d, (1518, y + 15), "Проект: «Северный свет»", 10, DIM, anchor="ra")
        hline(d, 40, 1560, y + 30, BORDER)
    return img, d


def content_top(menu: bool = True) -> int:
    return 122 if menu else 92


# --- главное окно ----------------------------------------------------------
def main_window():
    img, d = base_window("SVS-RVC · Студия поющего голоса", "Песня «Северный свет» · 48 кГц · 24 бит")
    top = content_top()

    # левая панель проекта
    rr(d, (40, top, 300, 976), 0, fill=PANEL)
    vline(d, 300, top, 976, BORDER)
    text(d, (62, top + 24), "ПРОЕКТ", 9, DIM, bold=True)
    text(d, (62, top + 44), "Северный свет", 13, TEXT, bold=True)
    text(d, (62, top + 64), "3:12 · 92 BPM · 4/4", 10, MUTED)

    y = top + 100
    for label, value, selected in (
        ("Партитура", None, False),
        ("Куплет 1", "64 такта", True),
        ("Припев", "32 такта", False),
        ("Бридж", "16 тактов", False),
        ("Лирика", "lyrics_ru.txt", False),
        ("Голос", "Анна_v2.rvc", False),
        ("Экспорт", "mixdown.wav", False),
    ):
        if value is None:
            text(d, (62, y), label, 10, DIM, bold=True)
            y += 26
            continue
        if selected:
            rr(d, (52, y - 4, 288, y + 32), 8, fill=ACCENT_SOFT, outline="#3b2f5c")
            d.rounded_rectangle((52, y + 2, 55, y + 26), 2, fill=ACCENT)
        text(d, (68, y), label, 11, TEXT if selected else "#c3cada", selected)
        if value:
            text(d, (68, y + 17), value, 9, MUTED)
        y += 44

    # карточка последнего рендера
    rr(d, (56, 806, 284, 922), 12, fill=PANEL_2, outline=BORDER)
    text(d, (72, 822), "Последний рендер", 9, DIM, bold=True)
    text(d, (72, 842), "Северный_свет_vocal.wav", 10, TEXT)
    text(d, (72, 862), "RTF 0.12 · 00:42", 9, MUTED)
    pill(GREEN, "Готово", 72, 884, d)
    text(d, (272, 894), "F5", 9, DIM, anchor="ra")

    # центральная область
    cx0, cx1 = 320, 1200
    # тулбар
    text(d, (cx0, top + 24), "Партитура", 16, TEXT, bold=True)
    chip(d, cx0 + 118, top + 20, "Куплет 1", TEXT, PANEL_3, 9, 10, 22)
    text(d, (cx1, top + 28), "Квантизация 1/16", 9, MUTED, anchor="ra")
    text(d, (cx1 - 130, top + 28), "Масштаб 100 %", 9, MUTED, anchor="ra")

    # панель партитуры
    sy0, sy1 = top + 58, 606
    rr(d, (cx0, sy0, cx1, sy1), 14, fill=PANEL, outline=BORDER)
    text(d, (cx0 + 18, sy0 + 14), "Куплет 1 · «Северный свет»", 11, TEXT, bold=True)
    text(d, (cx1 - 18, sy0 + 14), "G4 — C5 · сопрано", 9, MUTED, anchor="ra")

    gx0, gx1 = cx0 + 58, cx1 - 18
    gy0, gy1 = sy0 + 54, sy1 - 18
    rows = 12
    rh = (gy1 - gy0) / rows
    pitches = ["C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "B3", "A3", "G3", "F3"]
    # фон строк
    for r in range(rows):
        if r % 2 == 0:
            d.rectangle((gx0, gy0 + r * rh, gx1, gy0 + (r + 1) * rh), fill="#151922")
        text(d, (gx0 - 10, gy0 + r * rh + rh / 2), pitches[r], 8, DIM, anchor="rm")
    # сетка: 8 тактов, 4 доли
    cols = 32
    cw = (gx1 - gx0) / cols
    for c in range(cols + 1):
        x = gx0 + c * cw
        strong = c % 4 == 0
        d.line((x, gy0, x, gy1), fill="#2b3243" if strong else "#202532", width=1)
    for r in range(rows + 1):
        d.line((gx0, gy0 + r * rh, gx1, gy0 + r * rh), fill="#202532", width=1)
    # номера тактов
    for b in range(8):
        x = gx0 + b * 4 * cw
        text(d, (x + 4, gy0 - 16), str(b + 1), 8, DIM)
        d.line((x, gy0 - 4, x, gy0), fill="#3a4152", width=1)

    notes = [
        (0, 3, 2, "Се"), (2, 3, 2, "вер"), (4, 2, 4, "ный"),
        (8, 2, 2, "свет"), (10, 1, 2, "в"), (12, 0, 4, "не"),
        (16, 1, 2, "бе"), (18, 2, 2, "сах"), (20, 3, 4, "го"),
        (24, 3, 2, "рит"), (26, 2, 2, "наш"), (28, 1, 2, "путь"),
        (30, 0, 2, "мой"),
    ]
    for beat, pitch_row, dur, syllable in notes:
        x0 = gx0 + beat * cw + 2
        x1 = x0 + dur * cw - 4
        y0 = gy0 + pitch_row * rh + 5
        y1 = y0 + rh - 10
        selected = syllable == "бе"
        rr(d, (x0, y0, x1, y1), 4, fill=ACCENT if not selected else ACCENT_DARK,
           outline="#c4b5fd" if selected else None, width=2)
        if (x1 - x0) > 16:
            text(d, ((x0 + x1) / 2, (y0 + y1) / 2 + 1), syllable, 8, "#ffffff", True, anchor="mm")

    # плейхед
    px = gx0 + 17.5 * cw
    d.line((px, gy0 - 6, px, gy1), fill=CYAN, width=2)
    d.polygon([(px - 5, gy0 - 12), (px + 5, gy0 - 12), (px, gy0 - 5)], fill=CYAN)

    # панель лирики
    ly0, ly1 = sy1 + 14, sy1 + 104
    rr(d, (cx0, ly0, cx1, ly1), 12, fill=PANEL, outline=BORDER)
    text(d, (cx0 + 18, ly0 + 13), "Лирика", 10, DIM, bold=True)
    text(d, (cx1 - 18, ly0 + 13), "RU · 28 слогов", 9, MUTED, anchor="ra")
    syllables = ["Се", "вер", "ный", "свет", "в", "не", "бе", "сах", "го", "рит", "наш", "путь", "до", "мой"]
    sx = cx0 + 20
    for s in syllables:
        w = int(d.textlength(s, font=font(11, True))) + 18
        active = s == "бе"
        rr(d, (sx, ly0 + 40, sx + w, ly0 + 72), 8,
           fill=ACCENT_SOFT if active else PANEL_2,
           outline="#5b48a0" if active else None)
        text(d, (sx + w / 2, ly0 + 56), s, 11, "#d8ccff" if active else TEXT, active, anchor="mm")
        sx += w + 6

    # транспорт
    ty0, ty1 = ly1 + 14, 918
    rr(d, (cx0, ty0, cx1, ty1), 14, fill=PANEL, outline=BORDER)
    d.ellipse((cx0 + 22, ty0 + 24, cx0 + 74, ty0 + 76), fill=ACCENT)
    d.polygon([(cx0 + 43, ty0 + 37), (cx0 + 43, ty0 + 63), (cx0 + 61, ty0 + 50)], fill="#ffffff")
    text(d, (cx0 + 88, ty0 + 26), "00:42.318", 20, TEXT, bold=True)
    text(d, (cx0 + 190, ty0 + 36), "/ 03:12.000", 10, MUTED)
    text(d, (cx0 + 88, ty0 + 54), "Такт 15 · Доля 2", 9, MUTED)
    text(d, (cx0 + 88, ty0 + 70), "92 BPM · 4/4", 9, MUTED)

    # волновая форма
    wx0, wx1 = cx0 + 250, cx1 - 22
    wy = ty0 + 48
    d.line((wx0, wy, wx1, wy), fill="#2b3243")
    played_x = wx0 + (wx1 - wx0) * 0.22
    d.line((played_x, ty0 + 20, played_x, ty0 + 76), fill=CYAN, width=1)
    for i in range(int(wx1 - wx0)):
        t = i / (wx1 - wx0)
        amp = (0.35 + 0.65 * abs(math.sin(t * 37))) * (0.5 + 0.5 * abs(math.sin(t * 3.1)))
        if 0.18 < t < 0.3:
            amp *= 0.4
        h = int(amp * 16)
        x = wx0 + i
        color = "#6b5ab5" if t <= 0.22 else "#343b4d"
        d.line((x, wy - h, x, wy + h), fill=color)

    # кнопки транспорта
    bx = wx1 - 6
    for label in ("Метроном", "Цикл"):
        text(d, (bx, ty0 + 24), label, 9, MUTED, anchor="ra")
        bx -= 86

    # правая панель
    rx0, rx1 = 1220, 1540
    vline(d, 1200, top, 976, BORDER)
    text(d, (rx0, top + 24), "ГОЛОС", 9, DIM, bold=True)
    for i in range(3):
        dot(d, rx1 - 6 - i * 7, top + 30, 1.5, MUTED)

    rr(d, (rx0, top + 48, rx1, top + 196), 12, fill=PANEL_2, outline=BORDER)
    d.ellipse((rx0 + 16, top + 64, rx0 + 64, top + 112), fill="#4c3a8c")
    text(d, (rx0 + 40, top + 88), "А", 20, "#e9e2ff", True, anchor="mm")
    text(d, (rx0 + 76, top + 66), "Анна_v2", 14, TEXT, bold=True)
    text(d, (rx0 + 76, top + 86), "RVC v2 · 48 кГц", 9, MUTED)
    dot(d, rx0 + 80, top + 112, 3, GREEN)
    text(d, (rx0 + 90, top + 112), "Лицензия CC BY 4.0", 9, "#b9e8d5", anchor="lm")
    dot(d, rx0 + 80, top + 132, 3, GREEN)
    text(d, (rx0 + 90, top + 132), "Согласие до 31.12.2027", 9, "#b9e8d5", anchor="lm")

    rr(d, (rx0, top + 208, rx1, top + 244), 9, fill=PANEL, outline=BORDER)
    text(d, ((rx0 + rx1) / 2, top + 226), "Сменить модель", 10, TEXT, anchor="mm")

    hline(d, rx0, rx1, top + 266, BORDER)
    text(d, (rx0, top + 284), "Параметры переноса", 12, TEXT, bold=True)

    slider(d, rx0, top + 316, rx1 - rx0, 0.75, "Сила переноса", "75 %")
    slider(d, rx0, top + 376, rx1 - rx0, 0.50, "Питч-шифт", "+0 st")
    slider(d, rx0, top + 436, rx1 - rx0, 0.35, "Дыхательность", "35 %")
    slider(d, rx0, top + 496, rx1 - rx0, 0.50, "Формант", "0.0")

    text(d, (rx0, top + 552), "Пресет", 10, MUTED)
    rr(d, (rx0, top + 572, rx1, top + 610), 9, fill=PANEL, outline=BORDER)
    text(d, (rx0 + 14, top + 591), "Тёплый вокал", 10, TEXT, anchor="lm")
    d.line(((rx1 - 26, top + 588), (rx1 - 21, top + 593), (rx1 - 16, top + 588)), fill=MUTED, width=1)

    rr(d, (rx0, top + 630, rx1, top + 678), 10, fill=ACCENT)
    text(d, (rx0 + 18, top + 654), "Рендер", 13, "#ffffff", True, anchor="lm")
    text(d, (rx1 - 18, top + 654), "F5", 10, "#d9ccff", anchor="rm")
    rr(d, (rx0, top + 690, rx1, top + 734), 10, fill=PANEL, outline=BORDER)
    text(d, ((rx0 + rx1) / 2, top + 712), "Прослушать", 11, TEXT, anchor="mm")
    text(d, (rx0, top + 754), "Индекс включён · ratio 0.75", 9, DIM)
    text(d, (rx0, top + 772), "Кэш модели прогрет · 1.2 ГБ", 9, DIM)

    # статус-бар
    hline(d, 40, 1560, 936, BORDER)
    text(d, (62, 954), "Готово", 9, GREEN)
    dot(d, 110, 958, 3, GREEN)
    for i, item in enumerate(("RTF 0.12", "CPU 38 %", "Буфер 256", "48 кГц / 24 бит", "ASIO")):
        text(d, (330 + i * 140, 954), item, 9, MUTED)
    text(d, (1538, 954), "SVS-RVC 0.2.0", 9, DIM, anchor="ra")

    img.save(OUT / "main-window.png")
    return img


# --- диалог рендера -------------------------------------------------------
def render_dialog():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # затемнённый фон-приложение
    d.rectangle((0, 0, W, H), fill="#07090d")
    rr(d, (70, 40, 1530, 960), 20, fill="#0e1118", outline="#171b25")
    for i in range(9):
        d.rectangle((100, 100 + i * 80, 1500, 172 + i * 80), fill="#11151e")
    d.rectangle((0, 0, W, H), fill="#04060a")
    # модальное окно
    rr(d, (398, 132, 1202, 900), 20, fill=WIN, outline=BORDER)
    text(d, (436, 164), "Рендер вокальной партии", 22, TEXT, bold=True)
    text(d, (436, 200), "Песня «Северный свет» · Куплет 1 + Припев", 10, MUTED)
    text(d, (1162, 170), "×", 24, MUTED, anchor="mm")
    hline(d, 436, 1162, 230, BORDER)

    # формат
    text(d, (436, 254), "Формат", 12, TEXT, bold=True)
    text(d, (436, 284), "Тип файла", 10, MUTED)
    for i, label in enumerate(("WAV", "FLAC")):
        x0 = 700 + i * 110
        active = i == 0
        rr(d, (x0, 276, x0 + 100, 312), 8, fill=ACCENT if active else PANEL, outline=None if active else BORDER)
        text(d, (x0 + 50, 294), label, 10, "#ffffff" if active else MUTED, True, anchor="mm")

    text(d, (436, 336), "Частота дискретизации", 10, MUTED)
    for i, label in enumerate(("44.1 кГц", "48 кГц")):
        x0 = 700 + i * 120
        active = i == 1
        rr(d, (x0, 328, x0 + 110, 364), 8, fill=ACCENT if active else PANEL, outline=None if active else BORDER)
        text(d, (x0 + 55, 346), label, 10, "#ffffff" if active else MUTED, True, anchor="mm")

    text(d, (436, 388), "Разрядность", 10, MUTED)
    for i, label in enumerate(("16 бит", "24 бит")):
        x0 = 700 + i * 110
        active = i == 1
        rr(d, (x0, 380, x0 + 100, 416), 8, fill=ACCENT if active else PANEL, outline=None if active else BORDER)
        text(d, (x0 + 50, 398), label, 10, "#ffffff" if active else MUTED, True, anchor="mm")

    hline(d, 436, 1162, 442, BORDER)

    # параметры
    text(d, (436, 464), "Параметры экспорта", 12, TEXT, bold=True)
    options = (
        ("Нормализация громкости", "Цель −14 LUFS (EBU R128)", True),
        ("Экспортировать стем вокала", "Отдельный файл без инструментала", True),
        ("Маркировка «синтезировано»", "Метаданные + неслышимый водяной знак", True),
    )
    y = 496
    for title, sub, on in options:
        text(d, (436, y), title, 11, TEXT)
        text(d, (436, y + 18), sub, 9, DIM)
        switch(d, 1128, y + 2, on)
        y += 52

    hline(d, 436, 1162, 660, BORDER)

    # прогресс
    text(d, (436, 682), "Прогресс", 12, TEXT, bold=True)
    text(d, (436, 712), "Такт 42 из 64", 10, MUTED)
    text(d, (1162, 712), "68 %", 10, TEXT, bold=True, anchor="ra")
    rr(d, (436, 734, 1162, 746), 6, fill="#2b3243")
    rr(d, (436, 734, 436 + int(726 * 0.68), 746), 6, fill=ACCENT)
    text(d, (436, 760), "Осталось ~00:18 · RTF 0.11 · модель Анна_v2", 9, MUTED)
    rr(d, (436, 786, 1162, 818), 8, fill=PANEL)
    text(d, (450, 802), "exports/Северный_свет_vocal.wav", 9, "#b9c2d6", anchor="lm")

    # кнопки
    rr(d, (806, 838, 936, 878), 10, fill=PANEL, outline=BORDER)
    text(d, (871, 858), "Отмена", 11, TEXT, anchor="mm")
    rr(d, (956, 838, 1162, 878), 10, fill=ACCENT)
    text(d, (1059, 858), "Рендерить", 11, "#ffffff", True, anchor="mm")

    img.save(OUT / "render-dialog.png")
    return img


# --- live-монитор ----------------------------------------------------------
def live_monitor():
    img, d = base_window("SVS-RVC · Live-мониторинг", "Real-time озвучивание партии · ASIO · буфер 128")
    top = content_top()

    # левая карточка: метры и текущая нота
    rr(d, (60, top + 26, 900, top + 540), 16, fill=PANEL, outline=BORDER)
    text(d, (84, top + 46), "ВЫХОД · СТЕРЕО", 9, DIM, bold=True)
    pill(GREEN, "Live", 780, top + 40, d, GREEN, GREEN_SOFT)
    text(d, (84, top + 74), "Уровень сигнала", 11, MUTED)

    meter_x = [92, 182]
    meter_y0, meter_y1 = top + 106, top + 478
    for i, label in enumerate(("L", "R")):
        x0 = meter_x[i]
        x1 = x0 + 58
        rr(d, (x0, meter_y0, x1, meter_y1), 8, fill="#0e1118", outline=BORDER)
        # сегменты
        seg_h = 9
        gap = 3
        n = int((meter_y1 - meter_y0 - 16) / (seg_h + gap))
        level = 0.74 if i == 0 else 0.68
        for s in range(n):
            sy = meter_y1 - 8 - (s + 1) * (seg_h + gap)
            frac = s / n
            color = GREEN if frac < 0.62 else (AMBER if frac < 0.85 else RED)
            if frac > level:
                color = "#252b39"
            rr(d, (x0 + 10, sy, x1 - 10, sy + seg_h), 2, fill=color)
        text(d, (x0 + 29, meter_y1 + 16), label, 10, MUTED, anchor="mm")

    # шкала
    for i, mark in enumerate(("-60", "-40", "-20", "-12", "-6", "0")):
        yy = meter_y1 - 8 - (meter_y1 - meter_y0 - 16) * (i / 5)
        text(d, (254, yy), mark, 8, DIM, anchor="lm")
        d.line((244, yy, 250, yy), fill="#3a4152")

    # текущая нота
    text(d, (330, top + 116), "ТЕКУЩАЯ НОТА", 9, DIM, bold=True)
    text(d, (330, top + 140), "A4", 54, TEXT, bold=True)
    text(d, (430, top + 158), "«бе»", 20, "#c4b5fd", bold=True)
    text(d, (330, top + 210), "440.0 Гц · нота 17 из 64", 10, MUTED)
    text(d, (330, top + 236), "Анна_v2 · сила переноса 75 %", 10, MUTED)

    for i, (label, value, color) in enumerate((("Задержка", "12 мс", GREEN), ("XRUN", "0", GREEN), ("CPU", "42 %", AMBER))):
        x0 = 330 + i * 176
        rr(d, (x0, top + 286, x0 + 160, top + 360), 12, fill=PANEL_2, outline=BORDER)
        text(d, (x0 + 14, top + 300), label, 9, MUTED)
        text(d, (x0 + 14, top + 320), value, 20, color, True)

    # мини-история нот
    text(d, (330, top + 386), "Следующие ноты", 9, DIM, bold=True)
    hist = ("бе", "сах", "го", "рит", "наш", "путь", "до", "мой")
    sx = 330
    for i, s in enumerate(hist):
        active = i == 0
        w = int(d.textlength(s, font=font(9, True))) + 16
        rr(d, (sx, top + 408, sx + w, top + 434), 7, fill=ACCENT_SOFT if active else PANEL_2)
        text(d, (sx + w / 2, top + 421), s, 9, "#d8ccff" if active else MUTED, active, anchor="mm")
        sx += w + 5

    # F0-контур
    text(d, (330, top + 466), "F0-контур · последние 2 с", 9, DIM, bold=True)
    px0, px1 = 330, 860
    py0, py1 = top + 490, top + 520
    for g in range(3):
        gy = py0 + (py1 - py0) * g / 2
        d.line((px0, gy, px1, gy), fill="#202532", width=1)
    pts = []
    for i in range(64):
        x = px0 + (px1 - px0) * i / 63
        y = (py0 + py1) / 2 - 10 * math.sin(i / 5.5) - 4 * math.sin(i / 1.7)
        pts.append((x, y))
    d.line(pts, fill=ACCENT, width=2, joint="curve")
    dot(d, pts[-1][0], pts[-1][1], 4, CYAN)
    text(d, (px1 - 4, py0 - 2), "A4", 9, CYAN, True, anchor="ra")

    # правая карточка: настройки
    rr(d, (920, top + 26, 1540, top + 540), 16, fill=PANEL, outline=BORDER)
    text(d, (944, top + 46), "ВХОД И МОНИТОРИНГ", 9, DIM, bold=True)
    text(d, (944, top + 74), "MIDI-клавиатура", 11, MUTED)
    rr(d, (944, top + 96, 1516, top + 134), 9, fill=PANEL_2, outline=BORDER)
    text(d, (960, top + 115), "Arturia KeyLab 61 · подключена", 10, TEXT, anchor="lm")
    dot(d, 1498, top + 115, 3, GREEN)

    text(d, (944, top + 156), "Активная модель", 10, MUTED)
    rr(d, (944, top + 176, 1516, top + 252), 10, fill=PANEL_2, outline=BORDER)
    d.ellipse((958, top + 190, 994, top + 226), fill="#4c3a8c")
    text(d, (976, top + 208), "А", 13, "#e9e2ff", True, anchor="mm")
    text(d, (1008, top + 192), "Анна_v2", 11, TEXT, bold=True)
    text(d, (1008, top + 210), "RVC v2 · 48 кГц · индекс 0.75", 9, MUTED)
    text(d, (1008, top + 228), "Согласие подтверждено", 9, GREEN)

    text(d, (944, top + 276), "Параметры live", 10, MUTED)
    slider(d, 944, top + 304, 572, 0.5, "Питч-шифт", "+0 st")
    slider(d, 944, top + 360, 572, 0.35, "Дыхательность", "35 %")
    slider(d, 944, top + 416, 572, 0.2, "Реверб", "20 %")

    rr(d, (944, top + 476, 1222, top + 518), 10, fill=RED_SOFT, outline="#5c2a33")
    text(d, (1083, top + 497), "Стоп", 11, "#ffb4b4", True, anchor="mm")
    rr(d, (1238, top + 476, 1516, top + 518), 10, fill=PANEL_2, outline=BORDER)
    text(d, (1377, top + 497), "Записать демо", 11, TEXT, anchor="mm")

    # нижняя карточка: клавиатура
    rr(d, (60, 680, 1540, 930), 16, fill=PANEL, outline=BORDER)
    text(d, (84, 698), "MIDI-ВВОД", 9, DIM, bold=True)
    text(d, (1516, 698), "Октава C3 — C5", 9, MUTED, anchor="ra")

    kx0, kx1 = 84, 1516
    ky0, ky1 = 724, 898
    white = 21
    kw = (kx1 - kx0) / white
    for i in range(white):
        x0 = kx0 + i * kw
        rr(d, (x0, ky0, x0 + kw - 3, ky1), 5, fill="#f2f4f8", outline="#c9cfdb")
        if i % 7 in (0,):
            text(d, (x0 + kw / 2, ky1 - 14), f"C{3 + i // 7}", 8, "#6b7280", anchor="mm")
    # чёрные клавиши
    for i in range(white):
        if i % 7 in (0, 2, 4, 5):
            x = kx0 + (i + 1) * kw - 14
            rr(d, (x, ky0, x + 20, ky0 + 118), 4, fill="#151922", outline="#0a0d12")
    # подсветка нот A4/B4/C5 (примерно)
    for idx in (12, 14, 15):
        x0 = kx0 + idx * kw
        rr(d, (x0, ky0, x0 + kw - 3, ky1), 5, fill="#d8ccff", outline=ACCENT)
        text(d, (x0 + kw / 2, ky1 - 14), "A4" if idx == 12 else ("B4" if idx == 14 else "C5"), 8, "#4c3a8c", True, anchor="mm")

    text(d, (84, 948), "Вход: 48 кГц · 24 бит · задержка 12 мс", 9, MUTED)
    text(d, (1516, 948), "Поток стабилен · 0 срывов за 00:42", 9, GREEN, anchor="ra")
    img.save(OUT / "live-monitor.png")
    return img


# --- менеджер моделей ------------------------------------------------------
def model_manager():
    img, d = base_window("SVS-RVC · Менеджер моделей", "Библиотека RVC-тембров · лицензии и согласия")
    top = content_top()

    text(d, (60, top + 28), "Менеджер моделей", 22, TEXT, bold=True)
    text(d, (60, top + 62), "6 моделей · 4 готовы · 1 на проверке · 1 без согласия", 10, MUTED)
    rr(d, (1258, top + 34, 1540, top + 82), 10, fill=ACCENT)
    text(d, (1399, top + 58), "+  Импорт модели", 11, "#ffffff", True, anchor="mm")

    # поиск и фильтры
    rr(d, (60, top + 104, 560, top + 142), 9, fill=PANEL, outline=BORDER)
    d.ellipse((76, top + 116, 90, top + 130), outline=MUTED, width=1)
    d.line((88, top + 128, 94, top + 134), fill=MUTED, width=1)
    text(d, (102, top + 123), "Поиск по названию или владельцу…", 10, DIM, anchor="lm")
    for i, (label, active) in enumerate((("Все", True), ("Готовые", False), ("Без согласия", False))):
        x0 = 596 + i * 116
        rr(d, (x0, top + 108, x0 + 104, top + 138), 15, fill=ACCENT_SOFT if active else PANEL, outline="#4a3b78" if active else BORDER)
        text(d, (x0 + 52, top + 123), label, 9, "#c4b5fd" if active else MUTED, active, anchor="mm")

    # таблица
    tx0, tx1, ty0, ty1 = 60, 1300, top + 166, top + 760
    rr(d, (tx0, ty0, tx1, ty1), 14, fill=PANEL, outline=BORDER)
    cols = [(84, "МОДЕЛЬ"), (430, "ТЕМБР"), (640, "ЧАСТОТА"), (770, "ЛИЦЕНЗИЯ"), (980, "СОГЛАСИЕ"), (1160, "СТАТУС")]
    text(d, (84, ty0 + 24), "МОДЕЛЬ", 9, DIM, bold=True)
    for x, title in cols[1:]:
        text(d, (x, ty0 + 24), title, 9, DIM, bold=True)
    hline(d, tx0 + 1, tx1 - 1, ty0 + 46, BORDER)

    rows = [
        ("Анна_v2", "женский · лирический", "48 кГц", "CC BY 4.0", "до 31.12.2027", "Готова", True),
        ("Михаил_v1", "мужской · баритон", "48 кГц", "CC BY 4.0", "до 30.06.2027", "Готова", False),
        ("Demo_Choir", "хор · 4 голоса", "44.1 кГц", "CC0", "бессрочно", "Готова", False),
        ("Elena_v3", "женский · эстрадный", "48 кГц", "Proprietary", "до 01.03.2027", "Проверка", False),
        ("Rock_Lead", "мужской · рок", "40 кГц", "CC BY-NC", "нет", "Нет согласия", False),
        ("Whisper", "шёпот · текстура", "32 кГц", "CC0", "бессрочно", "Готова", False),
    ]
    y = ty0 + 58
    for name, timbre, rate, lic, consent, status, selected in rows:
        if selected:
            rr(d, (tx0 + 8, y - 6, tx1 - 8, y + 54), 9, fill=ACCENT_SOFT)
            d.rounded_rectangle((tx0 + 8, y - 2, tx0 + 11, y + 50), 2, fill=ACCENT)
        text(d, (84, y), name, 11, TEXT, bold=True)
        text(d, (430, y), timbre, 10, "#c3cada")
        text(d, (640, y), rate, 10, MUTED)
        text(d, (770, y), lic, 10, MUTED)
        text(d, (980, y), consent, 10, MUTED if consent != "нет" else RED)
        color, bg = (GREEN, GREEN_SOFT) if status == "Готова" else ((AMBER, AMBER_SOFT) if status == "Проверка" else (RED, RED_SOFT))
        w = int(d.textlength(status, font=font(9, True))) + 34
        rr(d, (1160, y - 4, 1160 + w, y + 20), 12, fill=bg)
        dot(d, 1172, y + 8, 3, color)
        text(d, (1180, y + 8), status, 9, color, True, anchor="lm")
        hline(d, tx0 + 12, tx1 - 12, y + 54, "#202532")
        y += 86

    # карточка выбранной модели
    dx0, dx1, dy0, dy1 = 1320, 1540, top + 166, top + 760
    rr(d, (dx0, dy0, dx1, dy1), 14, fill=PANEL, outline=BORDER)
    d.ellipse((dx0 + 22, dy0 + 24, dx0 + 86, dy0 + 88), fill="#4c3a8c")
    text(d, (dx0 + 54, dy0 + 56), "А", 26, "#e9e2ff", True, anchor="mm")
    text(d, (dx0 + 22, dy0 + 104), "Анна_v2", 14, TEXT, bold=True)
    text(d, (dx0 + 22, dy0 + 126), "женский · лирический", 9, MUTED)
    pill(GREEN, "Активна", dx0 + 22, dy0 + 148, d)

    fields = (
        ("Владелец", "А. Иванова"),
        ("Лицензия", "CC BY 4.0"),
        ("Согласие", "до 31.12.2027"),
        ("Частота", "48 кГц"),
        ("Формат", "RVC v2"),
        ("Хеш", "9f3c…a71d"),
    )
    fy = dy0 + 196
    for label, value in fields:
        text(d, (dx0 + 22, fy), label, 9, DIM)
        text(d, (dx1 - 22, fy), value, 10, TEXT, anchor="ra")
        hline(d, dx0 + 22, dx1 - 22, fy + 22, "#202532")
        fy += 46

    rr(d, (dx0 + 22, dy0 + 486, dx1 - 22, dy0 + 526), 9, fill=PANEL_2, outline=BORDER)
    text(d, ((dx0 + dx1) / 2, dy0 + 506), "Проверить целостность", 10, TEXT, anchor="mm")
    rr(d, (dx0 + 22, dy0 + 538, dx1 - 22, dy0 + 578), 9, fill=ACCENT)
    text(d, ((dx0 + dx1) / 2, dy0 + 558), "Сделать активной", 10, "#ffffff", True, anchor="mm")

    text(d, (60, 920), "Проверка модели включает хеш-сумму, версию RVC, частоту и наличие согласия владельца.", 9, DIM)

    img.save(OUT / "model-manager.png")
    return img


def use_case_diagram():
    """SysML v2 use case diagram (light theme, для печати)."""
    img = Image.new("RGB", (W, H), "#f5f6fa")
    d = ImageDraw.Draw(img)

    text(d, (80, 48), "SVS-RVC · варианты использования", 26, "#111827", bold=True)
    text(d, (80, 86), "SysML v2 use case model · бизнес-требования лабораторной работы №3", 11, "#6b7280")
    rr(d, (1400, 50, 1540, 84), 10, fill="#ede9fe", outline="#c4b5fd")
    text(d, (1470, 67), "SysML v2", 10, "#5b21b6", True, anchor="mm")

    # граница системы
    rr(d, (420, 140, 1180, 860), 18, fill="#ffffff", outline="#cbd5e1", width=2)
    text(d, (800, 166), "SVS-RVC", 17, "#0f172a", True, anchor="mm")
    text(d, (800, 190), "система синтеза поющего голоса", 9, "#64748b", anchor="mm")

    # связи актёров (рисуются до эллипсов)
    actor_line = "#94a3b8"
    d.line((250, 270, 680, 270), fill=actor_line, width=1)
    d.line((1380, 440, 1120, 440), fill=actor_line, width=1)
    d.line((250, 740, 480, 740), fill=actor_line, width=1)
    d.line((1380, 740, 1120, 740), fill=actor_line, width=1)

    # include / extend
    def dashed(p1, p2, color="#8b5cf6", dash=7, gap=5, width=1):
        x1, y1 = p1
        x2, y2 = p2
        length = math.hypot(x2 - x1, y2 - y1)
        if length == 0:
            return
        ux, uy = (x2 - x1) / length, (y2 - y1) / length
        pos = 0.0
        while pos < length:
            end = min(pos + dash, length)
            d.line((x1 + ux * pos, y1 + uy * pos, x1 + ux * end, y1 + uy * end), fill=color, width=width)
            pos = end + gap

    def arrow(p1, p2, color="#8b5cf6", size=7):
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        left = (p2[0] - size * math.cos(ang - 0.5), p2[1] - size * math.sin(ang - 0.5))
        right = (p2[0] - size * math.cos(ang + 0.5), p2[1] - size * math.sin(ang + 0.5))
        d.polygon([p2, left, right], fill=color)

    dashed((740, 312), (665, 398))
    arrow((740, 312), (665, 398))
    dashed((860, 312), (935, 398))
    arrow((860, 312), (935, 398))
    dashed((800, 542), (800, 328))
    arrow((800, 542), (800, 328))

    # варианты использования
    def uc(cx, cy, title, br):
        d.ellipse((cx - 130, cy - 48, cx + 130, cy + 48), fill="#eef2ff", outline="#8b5cf6", width=2)
        text(d, (cx, cy - 9), title, 12, "#1e1b4b", True, anchor="mm")
        text(d, (cx, cy + 16), br, 9, "#6d28d9", anchor="mm")

    uc(800, 270, "Создать вокальное демо", "BR-01 · BR-02")
    uc(600, 440, "Перенести тембр", "BR-03")
    uc(1000, 440, "Экспортировать в DAW", "BR-06")
    uc(800, 590, "Live-мониторинг", "BR-07")
    uc(600, 740, "Управлять моделями", "BR-08")
    uc(1000, 740, "Согласие и маркировка", "BR-05")

    # подписи стереотипов
    text(d, (694, 336), "«include»", 9, "#7c3aed")
    text(d, (886, 336), "«include»", 9, "#7c3aed")
    text(d, (812, 424), "«extend»", 9, "#7c3aed")

    # актёры
    def actor(cx, cy, lines):
        d.ellipse((cx - 11, cy - 54, cx + 11, cy - 32), outline="#334155", width=2)
        d.line((cx, cy - 32, cx, cy + 4), fill="#334155", width=2)
        d.line((cx - 22, cy - 18, cx + 22, cy - 18), fill="#334155", width=2)
        d.line((cx, cy + 4, cx - 16, cy + 30), fill="#334155", width=2)
        d.line((cx, cy + 4, cx + 16, cy + 30), fill="#334155", width=2)
        for i, line in enumerate(lines):
            text(d, (cx, cy + 42 + i * 17), line, 10, "#0f172a", True, anchor="mm")

    actor(220, 270, ("Композитор /", "продюсер"))
    actor(1380, 440, ("Звукорежиссёр",))
    actor(220, 740, ("Оператор", "моделей"))
    actor(1380, 740, ("Владелец голоса",))

    # пояснения
    hline(d, 80, 1520, 900, "#d7dbe6")
    text(d, (80, 918), "SysML v2 · use case diagram", 9, "#475569", bold=True)
    text(d, (80, 936), "BR-04 (локальная обработка) и BR-09 (отчёт о рендере) — сквозные ограничения, см. SRS 2.7 и 3.3.", 9, "#64748b")
    text(d, (1520, 918), "Мокапы: lab3/mockups/*.png", 9, "#64748b", anchor="ra")

    img.save(OUT / "use-case-diagram.png")
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (main_window, render_dialog, live_monitor, model_manager, use_case_diagram):
        fn()
        print("saved:", fn.__name__)


if __name__ == "__main__":
    main()

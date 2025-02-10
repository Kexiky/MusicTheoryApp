# config.py
# Конфигурация приложения

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

# Параметры нотного стана (узкий стан)
STAFF_X_START = 20
STAFF_X_END = 420
STAFF_WIDTH = STAFF_X_END - STAFF_X_START

TREBLE_STAFF_BOTTOM = 200  # нижняя линия скрипичного стана (например, E4)
BASS_STAFF_BOTTOM = 400    # нижняя линия басового стана (например, G2)
STAFF_LINE_SPACING = 10

VERTICAL_ADJUSTMENT = 10   # поправка для смещения ключевых символов вверх
NOTE_VERTICAL_SHIFT = 3    # сдвиг нот вниз (на пару пикселей)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
HIGHLIGHT = (173, 216, 230)  # светло-голубой для выделения

# Шрифты
MUSIC_FONT_NAME = "Segoe UI Symbol"
MUSIC_FONT_SIZE = 40
CLEF_FONT_SIZE = 60

TEXT_FONT_NAME = "Arial"
TEXT_FONT_SIZE = 20

# Тональности (ключевые знаки)
KEY_SIGNATURES = {
    "C":  {"accidental": None, "notes": []},
    "G":  {"accidental": "#",  "notes": ["F"]},
    "D":  {"accidental": "#",  "notes": ["F", "C"]},
    "A":  {"accidental": "#",  "notes": ["F", "C", "G"]},
    "E":  {"accidental": "#",  "notes": ["F", "C", "G", "D"]},
    "B":  {"accidental": "#",  "notes": ["F", "C", "G", "D", "A"]},
    "F":  {"accidental": "b",  "notes": ["B"]},
    "Bb": {"accidental": "b",  "notes": ["B", "E"]},
    "Eb": {"accidental": "b",  "notes": ["B", "E", "A"]},
    "Ab": {"accidental": "b",  "notes": ["B", "E", "A", "D"]},
}
DEFAULT_KEY = "C"

# Параметры для кругов квинтов
MAJOR_KEYS = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
MINOR_KEYS = ["Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m", "Bbm", "Fm", "Cm", "Gm", "Dm"]

# Параметры пиано
PIANO_NOTE_MIN = 24  # C3
PIANO_NOTE_MAX = 108  # C5
PIANO_HEIGHT = 50

# Область для кликабельного поля "Current Key" (x, y, ширина, высота)
CURRENT_KEY_RECT = (20, 10, 150, 30)

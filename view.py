# view.py
import pygame
import math
import config as cfg
from models import diatonic_number

# Инициализируем шрифты (предполагается, что pygame.font уже инициализирован)
music_font = pygame.font.SysFont(cfg.MUSIC_FONT_NAME, cfg.MUSIC_FONT_SIZE)
clef_font = pygame.font.SysFont(cfg.MUSIC_FONT_NAME, cfg.CLEF_FONT_SIZE)
text_font = pygame.font.SysFont(cfg.TEXT_FONT_NAME, cfg.TEXT_FONT_SIZE)

def get_note_y(letter, octave, clef):
    if clef == "treble":
        ref_letter, ref_octave = "E", 4
        base_y = cfg.TREBLE_STAFF_BOTTOM
    else:
        ref_letter, ref_octave = "G", 2
        base_y = cfg.BASS_STAFF_BOTTOM
    ref = diatonic_number(ref_letter, ref_octave)
    note_val = diatonic_number(letter, octave)
    offset = note_val - ref
    return base_y - (offset * (cfg.STAFF_LINE_SPACING / 2)) + cfg.NOTE_VERTICAL_SHIFT

def draw_staff(base_y, x_start, x_end):
    surface = pygame.display.get_surface()
    for i in range(5):
        y = base_y - i * cfg.STAFF_LINE_SPACING
        pygame.draw.line(surface, cfg.BLACK, (x_start, y), (x_end, y), 2)

def draw_clef(clef, x, base_y):
    surface = pygame.display.get_surface()
    symbol = "𝄞" if clef == "treble" else "𝄢"
    rendered = clef_font.render(symbol, True, cfg.BLACK)
    surface.blit(rendered, (x, base_y - 4 * cfg.STAFF_LINE_SPACING - cfg.VERTICAL_ADJUSTMENT))

def draw_key_signature(key_name, clef, x):
    surface = pygame.display.get_surface()
    key_data = cfg.KEY_SIGNATURES[key_name]
    if key_data["accidental"] == "#":
        accidental_symbol = "♯"
        vertical_treble_sub = cfg.TREBLE_STAFF_BOTTOM - cfg.VERTICAL_ADJUSTMENT
        vertical_bottom_sub = cfg.BASS_STAFF_BOTTOM - cfg.VERTICAL_ADJUSTMENT
        if clef == "treble":
            positions = [vertical_treble_sub - 0.5 * cfg.STAFF_LINE_SPACING,
                         vertical_treble_sub- 1.5 * cfg.STAFF_LINE_SPACING]
        else:
            positions = [vertical_bottom_sub - 0.5 * cfg.STAFF_LINE_SPACING,
                         vertical_bottom_sub - 1.5 * cfg.STAFF_LINE_SPACING]
        num = len(key_data["notes"])
        for i in range(num):
            pos_y = positions[i % len(positions)]
            rendered = music_font.render(accidental_symbol, True, cfg.BLACK)
            surface.blit(rendered, (x + i * 12, pos_y - 10))
    elif key_data["accidental"] == "b":
        accidental_symbol = "♭"
        if clef == "treble":

            positions = [vertical_treble_sub - 0.5 * cfg.STAFF_LINE_SPACING,
                         vertical_treble_sub - 1.5 * cfg.STAFF_LINE_SPACING,
                         vertical_treble_sub - 2.5 * cfg.STAFF_LINE_SPACING,
                         vertical_treble_sub - 3.5 * cfg.STAFF_LINE_SPACING]
        else:
            positions = [vertical_bottom_sub - 0.5 * cfg.STAFF_LINE_SPACING,
                         vertical_bottom_sub - 1.5 * cfg.STAFF_LINE_SPACING,
                         vertical_bottom_sub - 2.5 * cfg.STAFF_LINE_SPACING,
                         vertical_bottom_sub - 3.5 * cfg.STAFF_LINE_SPACING]
        num = len(key_data["notes"])
        for i in range(num):
            pos_y = positions[i % len(positions)]
            rendered = music_font.render(accidental_symbol, True, cfg.BLACK)
            surface.blit(rendered, (x + i * 12, pos_y - 10))

def draw_note(letter, accidental, octave, x):
    from models import diatonic_number
    natural_semitones = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    midi_base = (octave + 1) * 12 + natural_semitones[letter]
    if accidental == "#":
        midi_note = midi_base + 1
    elif accidental == "b":
        midi_note = midi_base - 1
    else:
        midi_note = midi_base
    clef = "treble" if midi_note >= 60 else "bass"
    y = get_note_y(letter, octave, clef)
    surface = pygame.display.get_surface()
    note_rect = pygame.Rect(x, y - 6, 12, 8)
    pygame.draw.ellipse(surface, cfg.BLACK, note_rect, 0)
    if y > ((cfg.TREBLE_STAFF_BOTTOM - 4 * cfg.STAFF_LINE_SPACING) if clef == "treble" else (cfg.BASS_STAFF_BOTTOM - 4 * cfg.STAFF_LINE_SPACING)):
        pygame.draw.line(surface, cfg.BLACK, (x + 12, y), (x + 12, y - 30), 2)
    else:
        pygame.draw.line(surface, cfg.BLACK, (x, y), (x, y + 30), 2)
    if accidental is not None:
        if accidental == "#":
            acc_symbol = "♯"
        elif accidental == "b":
            acc_symbol = "♭"
        elif accidental == "natural":
            acc_symbol = "♮"
        rendered = music_font.render(acc_symbol, True, cfg.BLACK)
        surface.blit(rendered, (x - 15, y - 10))
    if clef == "treble":
        base = cfg.TREBLE_STAFF_BOTTOM
        ref_letter, ref_octave = "E", 4
    else:
        base = cfg.BASS_STAFF_BOTTOM
        ref_letter, ref_octave = "G", 2
    ref_val = diatonic_number(ref_letter, ref_octave)
    note_val = diatonic_number(letter, octave)
    offset = note_val - ref_val
    if offset < 0:
        for pos in range(offset, 0):
            if pos % 2 == 0:
                ledger_y = base - (pos * (cfg.STAFF_LINE_SPACING / 2))
                pygame.draw.line(surface, cfg.BLACK, (x - 5, ledger_y), (x + 17, ledger_y), 2)
    elif offset >= 9:
        for pos in range(9, offset + 1, 2):
            ledger_y = base - (pos * (cfg.STAFF_LINE_SPACING / 2))
            pygame.draw.line(surface, cfg.BLACK, (x - 5, ledger_y), (x + 17, ledger_y), 2)

def draw_piano(current_notes, note_min=cfg.PIANO_NOTE_MIN, note_max=cfg.PIANO_NOTE_MAX):
    surface = pygame.display.get_surface()
    piano_height = cfg.PIANO_HEIGHT
    piano_y = surface.get_height() - piano_height
    piano_width = surface.get_width()
    white_keys = []
    for note in range(note_min, note_max + 1):
        if note % 12 in [0, 2, 4, 5, 7, 9, 11]:
            white_keys.append(note)
    num_white = len(white_keys)
    white_key_width = piano_width / num_white
    for i, note in enumerate(white_keys):
        x = i * white_key_width
        rect = pygame.Rect(x, piano_y, white_key_width, piano_height)
        if note in current_notes:
            pygame.draw.rect(surface, cfg.HIGHLIGHT, rect)
        else:
            pygame.draw.rect(surface, cfg.WHITE, rect)
        pygame.draw.rect(surface, cfg.BLACK, rect, 2)
    black_key_width = white_key_width * 0.6
    black_key_height = piano_height * 0.6
    for note in range(note_min, note_max + 1):
        if note % 12 in [1, 3, 6, 8, 10]:
            prev_white = None
            for w in white_keys:
                if w < note:
                    prev_white = w
                else:
                    break
            if prev_white is None:
                continue
            index = white_keys.index(prev_white)
            white_x = index * white_key_width
            x = white_x + white_key_width - black_key_width / 2
            rect = pygame.Rect(x, piano_y, black_key_width, black_key_height)
            if note in current_notes:
                pygame.draw.rect(surface, cfg.HIGHLIGHT, rect)
            else:
                pygame.draw.rect(surface, cfg.BLACK, rect)
            pygame.draw.rect(surface, cfg.BLACK, rect, 2)

def draw_circle_of_letters(
    keys,
    surface, center, radius, highlight,
    font_obj = pygame.font.SysFont('Arial', 20) 
):
    for i, key in enumerate(keys):
        angle = math.radians(90 - i * 30)
        x = center[0] + int(radius * math.cos(angle))
        y = center[1] - int(radius * math.sin(angle))
        label = font_obj.render(key, True, cfg.BLACK)
        label_rect = label.get_rect(center=(x, y))
        if highlight is not None and key == highlight:
            highlight_radius = label_rect.width // 2 + 5
            pygame.draw.circle(surface, cfg.HIGHLIGHT, label_rect.center, highlight_radius)
            label = font_obj.render(key, True, cfg.BLACK)
        surface.blit(label, label_rect)

def draw_circle_of_fifths_with_minor(center, outer_radius, inner_radius, highlight_major=None, highlight_minor=None):
    surface = pygame.display.get_surface()
    # Внешнее кольцо
    pygame.draw.circle(surface, cfg.LIGHT_GRAY, center, outer_radius + 40, 4)

    # Внешний круг (мажорные ключи)
    pygame.draw.circle(surface, cfg.BLACK, center, outer_radius, 2)
    font_obj = pygame.font.SysFont("Arial", 20)
    draw_circle_of_letters(
        keys=cfg.MAJOR_KEYS,
        surface=surface,
        center=center,
        radius=outer_radius+20,
        highlight=highlight_major,
        font_obj=font_obj
    )

    # Внутренний круг (минорные ключи)
    pygame.draw.circle(surface, cfg.BLACK, center, inner_radius, 2)
    draw_circle_of_letters(
        keys=cfg.MINOR_KEYS,
        surface=surface,
        center=center,
        radius=inner_radius+25,
        highlight=highlight_minor,
        font_obj=font_obj
    )

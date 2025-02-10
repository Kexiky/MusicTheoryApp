# controller.py
import pygame
from config import *
from config import KEY_SIGNATURES  # для смены тональности
from models import midi_to_note, analyze_chord_with_music21, get_chord_info, map_to_circle_key
from view import (draw_staff, draw_clef, draw_key_signature, draw_note, draw_piano,
                  draw_circle_of_fifths_with_minor)
import pygame.font

class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.current_notes = set()
        self.current_key = KEY_SIGNATURES.keys().__iter__().__next__()  # по умолчанию первый ключ, например "C"
        self.current_key = "C"  # или можно явно задать
    def process_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            # Циклическое переключение тональностей по цифрам
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                             pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                keys_order = list(KEY_SIGNATURES.keys())
                idx = keys_order.index(self.current_key)
                self.current_key = keys_order[(idx + 1) % len(keys_order)]
            # Виртуальная клавиатура
            key_map = {pygame.K_z: 60, pygame.K_s: 61, pygame.K_x: 62, pygame.K_d: 63,
                       pygame.K_c: 64, pygame.K_v: 65, pygame.K_g: 66, pygame.K_b: 67,
                       pygame.K_h: 68, pygame.K_n: 69, pygame.K_j: 70, pygame.K_m: 71,
                       pygame.K_q: 72}
            if event.key in key_map:
                self.current_notes.add(key_map[event.key])
        elif event.type == pygame.KEYUP:
            key_map = {pygame.K_z: 60, pygame.K_s: 61, pygame.K_x: 62, pygame.K_d: 63,
                       pygame.K_c: 64, pygame.K_v: 65, pygame.K_g: 66, pygame.K_b: 67,
                       pygame.K_h: 68, pygame.K_n: 69, pygame.K_j: 70, pygame.K_m: 71,
                       pygame.K_q: 72}
            if event.key in key_map:
                self.current_notes.discard(key_map[event.key])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(*CURRENT_KEY_RECT)
                if rect.collidepoint(event.pos):
                    keys_order = list(KEY_SIGNATURES.keys())
                    idx = keys_order.index(self.current_key)
                    self.current_key = keys_order[(idx + 1) % len(keys_order)]
        elif event.type == pygame.VIDEORESIZE:
            # Здесь можно обновлять размеры экрана, если требуется
            pass
        return True

    def render(self):
        # Отрисовка нотного стана и ключей
        draw_staff(TREBLE_STAFF_BOTTOM, STAFF_X_START, STAFF_X_START + STAFF_WIDTH)
        draw_clef("treble", 50, TREBLE_STAFF_BOTTOM)
        draw_key_signature(self.current_key, "treble", 100)
        draw_staff(BASS_STAFF_BOTTOM, STAFF_X_START, STAFF_X_START + STAFF_WIDTH)
        draw_clef("bass", 50, BASS_STAFF_BOTTOM)
        draw_key_signature(self.current_key, "bass", 100)
        # Отрисовка нот (по центру стана)
        key_data = KEY_SIGNATURES[self.current_key]
        for midi_val in self.current_notes:
            letter, accidental, octave = midi_to_note(midi_val, key_data)
            x_pos = STAFF_X_START + STAFF_WIDTH // 2
            draw_note(letter, accidental, octave, x_pos)
        # Отрисовка поля с названием аккорда (над пиано)
        surface = pygame.display.get_surface()
        chord_field_rect = pygame.Rect(STAFF_X_START, surface.get_height() - 120 - PIANO_HEIGHT, STAFF_WIDTH, 40)
        pygame.draw.rect(surface, LIGHT_GRAY, chord_field_rect)
        pygame.draw.rect(surface, BLACK, chord_field_rect, 2)
        chord_text = analyze_chord_with_music21(self.current_notes)
        # print(chord_text)
        chord_text = analyze_chord_with_music21(self.current_notes)
        if chord_text is None:
            chord_text = ""
        chord_surface = pygame.font.SysFont(TEXT_FONT_NAME, 20).render(str(chord_text), True, BLACK)


        surface.blit(chord_surface, (chord_field_rect.x + 5, chord_field_rect.y + 5))
        # Отрисовка кликабельного поля "Current Key"
        pygame.draw.rect(surface, LIGHT_GRAY, pygame.Rect(*CURRENT_KEY_RECT))
        pygame.draw.rect(surface, BLACK, pygame.Rect(*CURRENT_KEY_RECT), 2)
        key_surface = pygame.font.SysFont(TEXT_FONT_NAME, 20).render(f"Current Key: {self.current_key}", True, BLACK)
        surface.blit(key_surface, (CURRENT_KEY_RECT[0] + 5, CURRENT_KEY_RECT[1] + 5))
        # Отрисовка пиано
        draw_piano(self.current_notes)
        # Определение информации об аккорде для подсветки на круге
        chord_full_text = analyze_chord_with_music21(self.current_notes)
        root, quality = get_chord_info(chord_full_text)
        
        if root:
            if quality == "major":
                circle_major_key = map_to_circle_key(root)
                circle_minor_key = None
            elif quality == "minor":
                circle_major_key = None
                circle_minor_key = root + "m"
            else:
                circle_major_key = None
                circle_minor_key = None
        else:
            circle_major_key = None
            circle_minor_key = None
        # Отрисовка кварто-квинтового круга
        circle_center = (STAFF_X_END + 200, (TREBLE_STAFF_BOTTOM + BASS_STAFF_BOTTOM) // 2)
        outer_radius = 100
        inner_radius = outer_radius - 50
        draw_circle_of_fifths_with_minor(circle_center, outer_radius, inner_radius,
                                         highlight_major=circle_major_key,
                                         highlight_minor=circle_minor_key)

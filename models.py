# models.py
import logging
from music21 import chord as m21Chord, pitch as m21Pitch, harmony

logger = logging.getLogger(__name__)

def diatonic_number(letter, octave):
    order = "CDEFGAB"
    return octave * 7 + order.index(letter)

def midi_to_note(midi, key_data):
    note_index = midi % 12
    octave = midi // 12 - 1
    note_names_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_names_flat  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    if key_data and key_data.get("accidental") == "b":
        note_name = note_names_flat[note_index]
    else:
        note_name = note_names_sharp[note_index]
    if len(note_name) == 1:
        letter = note_name
        accidental = None
    else:
        letter = note_name[0]
        accidental = note_name[1]
    default_acc = key_data.get("accidental") if key_data and letter in key_data.get("notes", []) else None
    natural_semitones = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    natural_midi = (octave + 1) * 12 + natural_semitones[letter]
    if default_acc == "#":
        expected = natural_midi + 1
    elif default_acc == "b":
        expected = natural_midi - 1
    else:
        expected = natural_midi
    if midi == expected:
        return letter, None, octave
    else:
        if letter in key_data.get("notes", []):
            return letter, "natural", octave
        else:
            return letter, accidental, octave

def midi_to_name(midi):
    note_names_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = midi // 12 - 1
    return note_names_sharp[midi % 12] + str(octave)

def analyze_chord_with_music21(note_set):
    if not note_set:
        logger.info("Empty note set provided for chord analysis.")
        return ""
    chord_obj = m21Chord.Chord(note_set)
    chord_str = chord_obj.pitchedCommonName or "Неизвестный аккорд"
    return chord_str

def get_chord_info(chord_text):
    # Приводим значение к строке, если оно не строка
    chord_str = str(chord_text) if not isinstance(chord_text, str) else chord_text
    if not chord_str:
        return (None, None)
    
    root = chord_str[0] if ('#' not in chord_str) and ('b' not in chord_str) else chord_str[:2]
    quality = "major"
    if len(chord_str) <= 1:
        return (root, quality)
    
    quality = 'major' if 'major' in chord_str else "minor"
    return (root, quality)

def map_to_circle_key(root):
    mapping = {"C#": "Db", "D#": "Eb", "Gb": "F#", "G#": "Ab", "A#": "Bb"}
    mapped = mapping.get(root, root)
    logger.info("Mapping root %s to circle key: %s", root, mapped)
    return mapped

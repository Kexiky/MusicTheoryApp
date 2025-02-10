# midi_handler.py
import pygame.midi
import logging

logger = logging.getLogger(__name__)

class MidiHandler:
    def __init__(self):
        self.midi_input = None
        if pygame.midi.get_count() > 0:
            try:
                default_id = pygame.midi.get_default_input_id()
                self.midi_input = pygame.midi.Input(default_id)
                logger.info("MIDI Input device opened with id %s", default_id)
            except Exception as e:
                logger.exception("Error opening MIDI device: %s", e)
    
    def poll(self):
        if self.midi_input is not None and self.midi_input.poll():
            return self.midi_input.read(10)
        return []
    
    def close(self):
        if self.midi_input is not None:
            self.midi_input.close()
            logger.info("MIDI Input device closed")

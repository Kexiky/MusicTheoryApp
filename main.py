# main.py
import sys
import pygame
pygame.init()
import pygame.midi
import logging
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from controller import Controller
from midi_handler import MidiHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    pygame.init()
    pygame.midi.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Music Theory App")
    clock = pygame.time.Clock()

    controller = Controller(screen)
    midi_handler = MidiHandler()

    running = True
    while running:
        for event in pygame.event.get():
            if not controller.process_event(event):
                running = False

        # Обработка MIDI-событий
        midi_events = midi_handler.poll()
        for m_e in midi_events:
            data = m_e[0]
            status = data[0]
            note = data[1]
            velocity = data[2]
            if status == 144:  # Note On
                if velocity > 0:
                    controller.current_notes.add(note)
                    logger.info("MIDI Note On: %s", note)
                else:
                    controller.current_notes.discard(note)
                    logger.info("MIDI Note Off (velocity 0): %s", note)
            elif status == 128:
                controller.current_notes.discard(note)
                logger.info("MIDI Note Off: %s", note)

        screen.fill(WHITE)
        controller.render()
        pygame.display.flip()
        clock.tick(30)

    midi_handler.close()
    pygame.midi.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

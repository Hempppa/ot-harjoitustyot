import pygame

class Clock:
    """Luokka joka toimii sovelluksen kannalta kuin pygame.time.Clock()
    
    Attribute:
        clock: pygame.time.Clock() olio
    """
    def __init__(self):
        self._clock = pygame.time.Clock()

    def tick(self, fps):
        self._clock.tick(fps)

    def get_ticks(self):
        return pygame.time.get_ticks()

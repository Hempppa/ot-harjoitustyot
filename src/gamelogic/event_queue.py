import pygame

class EventQueue:
    """Luokka jolla ladataan käyttäjän syötteet
    """
    def get(self):
        return pygame.event.get()

    def wait(self):
        return pygame.event.wait()

import pygame

class EventQueue:
    def get(self):
        return pygame.event.get()

    def wait(self):
        return pygame.event.wait()

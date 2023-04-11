import pygame


class StartRenderer:
    def __init__(self, display):
        self._display = display
        self.base_font = pygame.font.Font(None, 32)

    def render(self):
        self._display.fill((200,200,200))
        start_rect = pygame.Rect(200,200,140,34)
        pygame.draw.rect(self._display, (100,100,100), start_rect)
        start_text = self.base_font.render("Start", True, (255,255,255))
        self._display.blit(start_text, (start_rect.x+2, start_rect.y+2))
        pygame.display.update()
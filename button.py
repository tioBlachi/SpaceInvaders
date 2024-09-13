import pygame
from constants import MAIN_MENU_FONT, WHITE

class Button:
    def __init__(self, text, x_pos, y_pos, screen, enabled):
        self.enabled = enabled
        self.screen = screen
        self.text = text
        self.x = x_pos
        self.y = y_pos

    def draw(self):
        button_text = MAIN_MENU_FONT.render(self.text, True, WHITE)
        button_rect = pygame.Rect((self.x, self.y), (button_text.get_width(), button_text.get_height()))
        if self.check_click():
            button_text = MAIN_MENU_FONT.render(self.text, True, 'light gray')
        else:
            button_text = MAIN_MENU_FONT.render(self.text, True, WHITE)
        pygame.draw.rect(self.screen, 'black', button_rect, 0, 5)
        #pygame.draw.rect(self.screen, WHITE, button_rect, 2, 5)
        self.screen.blit(button_text, (self.x + 5, self.y + 3))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect((self.x, self.y), (MAIN_MENU_FONT.render(self.text, True, WHITE).get_width(), MAIN_MENU_FONT.render(self.text, True, WHITE).get_height()))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        return False

from constants import MAIN_MENU_FONT, WHITE
from functions import start_game
from button import Button
import pygame
import os

def main():
    pygame.init()
    WIDTH, HEIGHT = 750, 750
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space Invaders')

    # Load assets
    bg_image = pygame.image.load(os.path.join('assets', 'images', 'moon_bg.jpg'))
    pygame.mixer.music.load(os.path.join('assets', 'music', 'OutThere.ogg'))
    pygame.mixer.music.play(-1)

    # Set up font
    text = MAIN_MENU_FONT.render('Space Invaders', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + text.get_height() // 2))  # Start below the screen

    # Set up scrolling speed
    scroll_speed = 2.75

    start_button = Button("START", 200, HEIGHT // 2 - 25, SCREEN, True)
    quit_button = Button("QUIT", 200, HEIGHT // 2 + 100, SCREEN, True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or quit_button.check_click():
                running = False
            if start_button.check_click():
                start_game(SCREEN)
                return  # Exit the main menu if game starts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game(SCREEN)

        SCREEN.blit(bg_image, (0, 0))

        # Update text position
        text_rect.y -= scroll_speed
        if text_rect.y <= HEIGHT // 3 - 60:
            scroll_speed = 0
            text_rect.y = HEIGHT // 3 - 60
            start_button.draw()
            quit_button.draw()

        SCREEN.blit(text, text_rect)

        if text_rect.bottom < 0:
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

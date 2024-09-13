import pygame
import os

pygame.init()

WIDTH = 750
HEIGHT = 750
FONT_SIZE = 50
WHITE = (255, 255, 255)
FPS = 60

DIFFICULTY = 3
SCORE = 0

P_DAMAGE_SFX = pygame.mixer.Sound(os.path.join('assets','sounds', 'hit01.wav'))
P_L_DAMAGE_SFX = pygame.mixer.Sound(os.path.join('assets','sounds', 'L_damage.wav'))
P_LASER_SFX = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'playerLaser.wav'))
P_LASER_SFX.set_volume(0.25)
E_LASER_SFX = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'enemy_laser.mp3'))
E_LASER_SFX.set_volume(0.25)
E_EXPLOSION_SFX = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosion.wav'))
E_EXPLOSION_SFX.set_volume(0.25)
P_MINUS_1_SFX = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'minus1.mp3'))
P_MINUS_1_SFX.set_volume(0.1)
BULLET_COL_SFX = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'rumble.flac'))
BULLET_COL_SFX.set_volume(0.25)

COLLISION_DELAY = 900
P_FLASH_DURATION = 750
P_FLASH_INTERVAL = 100

MAIN_MENU_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'main_menu_font.ttf'), 64)
FONT_PATH = pygame.font.Font(os.path.join('assets', 'fonts', 'suse_semi_bold.ttf'), 32)
DISPLAY_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'suse_semi_bold.ttf'), 42)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'background.png')), (WIDTH, HEIGHT))

PLAYER_VEL = 7
COOLDOWN = 500
LASER_VEL_P = 4
ENEMY_VEL = 4
LASER_VEL_E = 6

SHAKE_INTENSITY = 10
SHAKE_DURATION = 0.25

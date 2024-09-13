from turtle import Screen

import pygame
import random
import os
from button import Button
from constants import WIDTH, HEIGHT, BACKGROUND, PLAYER_VEL, ENEMY_VEL, LASER_VEL_P, LASER_VEL_E, P_LASER_SFX, \
    P_DAMAGE_SFX, FPS, FONT_PATH, WHITE, E_EXPLOSION_SFX, SHAKE_INTENSITY, SHAKE_DURATION, COLLISION_DELAY, \
    DISPLAY_FONT, MAIN_MENU_FONT, P_MINUS_1_SFX, COOLDOWN, BULLET_COL_SFX, P_L_DAMAGE_SFX, E_LASER_SFX
from game_state import game_state

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'xwing.png')), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.max_health = 100
        self.score = 0

    def health_bar(self, surface):
        width = 80
        height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y + 75

        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, width, height))
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, width * health_percentage, height))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_VEL
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_VEL
            if self.rect.x > WIDTH - self.rect.width:
                self.rect.x = WIDTH - self.rect.width

player = Player(WIDTH // 2 - 40, HEIGHT - 100)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_bullets, all_sprites):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'enemy_black.png')), (80, 80)), 270)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_shot_time = 0
        self.cooldown = random.randint(2000, 5000)
        self.enemy_bullets = enemy_bullets
        self.all_sprites = all_sprites

    def update(self):
        self.rect.y += ENEMY_VEL
        if self.rect.y > HEIGHT + 100:
            self.rect.x = random.randint(0, WIDTH - 80)
            self.rect.y = -100

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.cooldown:
            if player.rect.centerx - 10 <= self.rect.centerx <= player.rect.centerx + 10 and self.rect.top > 0:
                e_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                self.enemy_bullets.add(e_bullet)
                self.all_sprites.add(e_bullet)
                E_LASER_SFX.play()
                self.last_shot_time = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'player_laser.png')), (50, 75)), 90)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def update(self):
        self.rect.y -= LASER_VEL_P
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'enemy_laser.png')), (50, 75)), 270)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)

    def update(self):
        self.rect.y += LASER_VEL_E
        if self.rect.top > HEIGHT:
            self.kill()

def screen_shake(screen, intensity, duration):
    # such a cool effect
    original_surface = screen.copy()
    shake_frames = int(duration * FPS)

    for _ in range(shake_frames):
        screen.fill((0, 0, 0))
        x_offset = random.randint(-intensity, intensity)
        y_offset = random.randint(-intensity, intensity)
        screen.blit(original_surface, (x_offset, y_offset))
        pygame.display.flip()
        pygame.time.delay(int(1000 / FPS))

    screen.blit(original_surface, (0, 0))
    pygame.display.flip()

def mask(image):
    pygame.display.init()
    image = pygame.Surface.convert_alpha(image)
    return pygame.mask.from_surface(image)

def pixel_collision(obj1, obj2):
    mask1 = mask(obj1.image)
    mask2 = mask(obj2.image)
    offset_x = obj2.rect.left - obj1.rect.left
    offset_y = obj2.rect.top - obj1.rect.top
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None

def game_over():
    pygame.mixer.music.load(os.path.join('assets', 'music', 'kaiba.mp3'))
    pygame.mixer.music.play()
    screen = pygame.display.get_surface()
    text = MAIN_MENU_FONT.render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    player.score = 0
    game_state.difficulty = 3
    player.health = 100
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    restart()


def win():
    pygame.mixer.music.load(os.path.join('assets', 'music', 'victory.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    screen = pygame.display.get_surface()
    text = FONT_PATH.render(f'Level {game_state.difficulty - 2} Complete!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    game_state.increase_difficulty()
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(4200)
    pygame.mixer.music.stop()
    next_level()

def restart():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Next Level')

    quit_button = Button("QUIT", WIDTH // 2 - 75, HEIGHT // 2 - 25, SCREEN, True)
    restart_button = Button("RESTART", WIDTH // 2 - 75, HEIGHT // 2 - 100, SCREEN, True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if restart_button.check_click():
                running = False
                break
            if quit_button.check_click():
                running = False
                credits_roll()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    break
                if event.key == pygame.K_ESCAPE:
                    running = False
                    credits_roll()
                    pygame.quit()

        SCREEN.fill((0, 0, 0))
        restart_button.draw()
        quit_button.draw()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        player.rect.midtop = (WIDTH // 2, HEIGHT - 100)

    start_game(SCREEN)

def next_level():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Next Level')

    quit_button = Button("QUIT", WIDTH // 2 - 75, HEIGHT // 2 - 25, SCREEN, True)
    continue_button = Button("CONTINUE", WIDTH // 2 - 75, HEIGHT // 2 - 100, SCREEN, True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if continue_button.check_click():
                running = False
                break
            if quit_button.check_click():
                running = False
                credits_roll()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    break
                if event.key == pygame.K_ESCAPE:
                    running = False
                    credits_roll()
                    pygame.quit()

        SCREEN.fill((0, 0, 0))
        continue_button.draw()
        quit_button.draw()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        player.rect.midtop = (WIDTH // 2, HEIGHT - 100)

    start_game(SCREEN)

def credits_roll():
    pygame.mixer.music.load(os.path.join('assets', 'music', 'anime-chill.mp3'))
    pygame.mixer.music.play(-1)
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Thank You')

    text = FONT_PATH.render('Thank You For Playing!', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + text.get_height() // 2))
    scroll_speed = 3.5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill((0, 0, 0))
        text_rect.y -= scroll_speed
        SCREEN.blit(text, text_rect)

        if text_rect.bottom < 0:
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

def start_game(SCREEN):
    pygame.mixer.music.load(os.path.join('assets', 'music', 'space_shooter.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Space Invaders')

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player_group.add(player)
    all_sprites.add(player)

    for _ in range(game_state.difficulty):
        enemy = Enemy(random.randint(0, WIDTH - 80), random.randint(-1500, -100), enemy_bullets, all_sprites)
        enemies.add(enemy)
        all_sprites.add(enemy)

    for enemy in enemies:
        from constants import ENEMY_VEL
        for _ in range(game_state.difficulty):
            if 10 <= player.score <= 20:
                ENEMY_VEL += random.randint(ENEMY_VEL + 1, ENEMY_VEL + 3)

    clock = pygame.time.Clock()

    last_shot_time = 0
    last_collision_time = 0
    last_enemy_shot = 0
    e_shot_cooldown = 2000

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_w]:
            if current_time - last_shot_time > COOLDOWN:
                bullet = Bullet(player.rect.centerx, player.rect.centery)
                bullets.add(bullet)
                all_sprites.add(bullet)
                P_LASER_SFX.play()
                last_shot_time = current_time

        # enemy bullet and player bullet collision
        for bullet in bullets:
            for e_bullets in enemy_bullets:
                if pixel_collision(bullet, e_bullets):
                    BULLET_COL_SFX.play()
                    bullet.kill()
                    e_bullets.kill()

        # enemy bullet and player collision
        for e_bullet in enemy_bullets:
            if pixel_collision(player, e_bullet):
                current_time = pygame.time.get_ticks()
                if current_time - last_collision_time > COLLISION_DELAY:
                    P_L_DAMAGE_SFX.play()
                    player.health -= 15
                    screen_shake(SCREEN, SHAKE_INTENSITY, SHAKE_DURATION)
                    last_collision_time = current_time

        # player and enemy collision
        for enemy in enemies:
            if pixel_collision(player, enemy):
                current_time = pygame.time.get_ticks()
                if current_time - last_collision_time > COLLISION_DELAY:
                    screen_shake(SCREEN, SHAKE_INTENSITY, SHAKE_DURATION)
                    P_DAMAGE_SFX.play()
                    player.health -= 10
                    last_collision_time = current_time

        # bullet and enemy collision
        for bullet in bullets:
            for enemy in enemies:
                if pixel_collision(bullet, enemy):
                    bullet.kill()
                    enemy.kill()
                    E_EXPLOSION_SFX.play()
                    player.score += 1
                    if len(enemies) == 0:
                        pygame.time.wait(250)

        for enemy in enemies:
            if enemy.rect.top >= HEIGHT:
                player.score -= 1
                enemy.kill()
                P_MINUS_1_SFX.play()
                new_enemy = Enemy(random.randint(0, WIDTH - 80), -100, enemy_bullets, all_sprites)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                if player.score <= 0:
                    player.health -= 10
                    player.score = 0



        all_sprites.update()

        if player.health <= 0:
            game_over()
            return

        if len(enemies) == 0:
            win()
            return

        SCREEN.blit(BACKGROUND, (0, 0))
        player.health_bar(SCREEN)
        all_sprites.draw(SCREEN)

        level_font = DISPLAY_FONT.render(f'Level: {game_state.difficulty - 2}', True, WHITE)
        level_rect = level_font.get_rect(topright=(WIDTH - 10, 10))
        score_font = DISPLAY_FONT.render(f'Score: {player.score}', True, WHITE)
        score_rect = score_font.get_rect(topleft=(10, 10))
        SCREEN.blit(score_font, score_rect)
        SCREEN.blit(level_font, level_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
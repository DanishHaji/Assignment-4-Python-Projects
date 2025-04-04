import pygame
import random
import sys
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

clock = pygame.time.Clock()

# Load sounds
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('shoot.mp3')
collision_sound = pygame.mixer.Sound('explosion.mp3')
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Loop music

# Dynamic stars for background
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]

def draw_background():
    for star in stars:
        pygame.draw.circle(window, WHITE, star, 2)
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = random.randint(-20, -1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        shoot_sound.play()
        return bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 7
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

        # Enemy shoots randomly
        if random.randint(0, 100) < 5:
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 60))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = -100
        self.health = 20
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.top = -100
        if self.health <= 0:
            collision_sound.play()
            self.kill()

def main():
    global all_sprites, enemy_bullets, power_ups

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    player_lives = 3

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Background drawing
        window.fill(BLACK)
        draw_background()

        all_sprites.update()

        # Bullet-Enemy collision
        for bullet in bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in enemy_hits:
                score += 10
                bullet.kill()
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        # Enemy-Player collision
        enemy_hits_player = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_hits_player:
            player_lives -= 1
            if player_lives <= 0:
                running = False

        # Enemy bullets hitting player
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if player_hits:
            player_lives -= 1
            if player_lives <= 0:
                running = False

        # Spawn Power-ups
        if random.randint(0, 100) < 2:  # 2% chance to spawn
            power_up = PowerUp(random.randint(0, WIDTH), 0)
            all_sprites.add(power_up)
            power_ups.add(power_up)

        # Power-up collision
        power_up_collision = pygame.sprite.spritecollide(player, power_ups, True)
        if power_up_collision:
            player_lives += 1

        # Boss Battle
        if score == 100 and len(enemies) == 0:
            boss = Boss()
            all_sprites.add(boss)
            enemies.add(boss)

        all_sprites.draw(window)

        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(lives_text, (10, 40))

        pygame.display.flip()

    # Game Over screen
    font = pygame.font.SysFont('Arial', 36)
    game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
    window.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False
                main()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

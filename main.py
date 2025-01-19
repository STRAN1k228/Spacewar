import pygame
import random
import sqlite3


def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()


pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)

background = pygame.image.load('data/background.png')
player_image = pygame.image.load('data/player.png')
enemy_image = pygame.image.load('data/enemy.png')
boss_image = pygame.image.load('data/boss.png')
powerup_image = pygame.image.load('data/powerup.png')
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed



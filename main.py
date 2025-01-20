import pygame
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox


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


def register_user(username, password):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        start_game()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")


def registration_window():
    window = tk.Tk()
    window.title("Регистрация / Вход")
    window.geometry("400x400")  # Установка размера окна

    tk.Label(window, text="Имя пользователя").pack(pady=10)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Пароль").pack(pady=10)
    password_entry = tk.Entry(window, show='*')
    password_entry.pack(pady=5)

    tk.Button(window, text="Зарегистрироваться",
              command=lambda: register_user(username_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(window, text="Войти", command=lambda: open_login_window()).pack(pady=10)

    window.mainloop()


def open_login_window():
    login_window = tk.Tk()
    login_window.title("Вход")
    login_window.geometry("400x400")  # Установка размера окна

    tk.Label(login_window, text="Имя пользователя").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Пароль").pack(pady=10)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Войти", command=lambda: login_user(username_entry.get(), password_entry.get())).pack(
        pady=10)
    tk.Button(login_window, text="Назад к регистрации",
              command=lambda: [login_window.destroy(), registration_window()]).pack(pady=10)

    login_window.mainloop()


def start_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)

    background = pygame.image.load('data/background.png')
    player_image = pygame.image.load('data/player.png')
    enemy_image = pygame.image.load('data/enemy.png')
    shot = pygame.image.load('data/shot.png')
    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.play(-1)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = player_image
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.speed = 5
            self.double_shot = False

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed

        def fire(self):
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet1)
            if self.double_shot:
                bullet2 = Bullet(self.rect.centerx - 10, self.rect.top)
                bullet3 = Bullet(self.rect.centerx + 10, self.rect.top)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((5, 10))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = -10

        def update(self):
            self.rect.y += self.speed
            if self.rect.bottom < 0:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
            self.speed = random.randint(2, 5)

        def update(self):
            self.rect.y += self.speed
            if self.rect.top > HEIGHT:
                self.kill()

    class PowerUp(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = shot
            self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
            self.speed = 3

        def update(self):
            self.rect.y += self.speed
            if self.rect.top > HEIGHT:
                self.kill()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire()

        all_sprites.update()

        if random.random() < 0.02:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        if random.random() < 0.01:
            powerup = PowerUp()
            all_sprites.add(powerup)
            powerups.add(powerup)

        if pygame.sprite.spritecollide(player, enemies, True):
            messagebox.showerror("Игра окончена", "Вы проиграли!")
            running = False

        if pygame.sprite.spritecollide(player, powerups, True):
            player.double_shot = True

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


init_db()
registration_window()

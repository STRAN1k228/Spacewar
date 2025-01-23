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
        open_game_window()  # Открываем игру после успешной регистрации
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
        open_game_window()  # Открываем игру после успешного входа
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
        registration_window()  # Возвращаем на окно регистрации


def registration_window():
    window = tk.Tk()
    window.title("Регистрация")
    window.geometry("400x400")

    tk.Label(window, text="Имя пользователя").pack(pady=10)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Пароль").pack(pady=10)
    password_entry = tk.Entry(window, show='*')
    password_entry.pack(pady=5)

    tk.Button(window, text="Зарегистрироваться",
              command=lambda: register_user(username_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(window, text="Войти", command=lambda: [window.destroy(), open_login_window()]).pack(pady=10)

    window.mainloop()


def open_login_window():
    login_window = tk.Tk()
    login_window.title("Вход")
    login_window.geometry("400x400")

    tk.Label(login_window, text="Имя пользователя").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Пароль").pack(pady=10)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Войти", command=lambda: login_user(username_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(login_window, text="Назад к регистрации",
              command=lambda: [login_window.destroy(), registration_window()]).pack(pady=10)

    login_window.mainloop()


hight_win = 800
widght_win = 1200
widght_Gera = 40
wight_enemy = 70
total_score = 0
mod_fire = 1
Enemy_amount = 5

pygame.init()
font1 = pygame.font.Font(None, 36)
font2 = pygame.font.SysFont('corbel', 30)

class gamesprite(pygame.sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, pl_speed, pl_height, pl_widght):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(pl_image), (pl_height, pl_widght))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.name_image = pl_image

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def change_im(self, picture):
        self.image = pygame.transform.scale(pygame.image.load(picture), (self.rect.width, self.rect.height))
        self.name_image = picture

class player(gamesprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x < widght_win - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self, update_level):
        if update_level == 1:
            bullets.add(Fire('image/shot.png', self.rect.centerx, self.rect.top, 5, 20, 30))
        if update_level == 2:
            bullets.add(Fire('image/shot.png', self.rect.centerx + 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx - 10, self.rect.top, 5, 20, 30))
        if update_level == 3:
            bullets.add(Fire('image/shot.png', self.rect.centerx + 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx - 10, self.rect.top, 5, 20, 30))
            bullets.add(Fire('image/shot.png', self.rect.centerx + 30, self.rect.top, 5, 20, 30))

class Enemy(gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > hight_win:
            self.rect.y = random.randint(-300, 0)
            self.rect.x = random.randint(0, widght_win - self.rect.width)

class Fire(gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Bonus(gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.kill()

class Meteor(gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.kill()

def m_restart():
    global total_score
    total_score = 0
    global mod_fire
    gr_bonus.empty()
    ye_bonus.empty()
    meteorit.empty()
    Enemies.empty()
    mod_fire = 1
    hero.change_im('image/spaceshatel.png')

def open_game_window():
    global window
    window = pygame.display.set_mode((widght_win, hight_win))
    pygame.display.set_caption("Звёздные войны")
    run_game()

def run_game():
    global total_score, mod_fire, stop_game
    total_score = 0
    mod_fire = 1
    stop_game = False

    global hero
    hero = player('image/spaceshatel.png', 370, 600, 5, 100, 150)
    for i in range(5):
        Enemies.add(Enemy('image/enemyship.png', random.randint(0, widght_win - wight_enemy) - 100, random.randint(0, 1000) * -1, random.randint(3, 5), wight_enemy, wight_enemy))

    clock = pygame.time.Clock()
    FPS = 60
    background = pygame.transform.scale(pygame.image.load("image/background.png"), (widght_win, hight_win))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    fire_sound.play()
                    hero.fire(mod_fire)

        if stop_game:
            end_score2 = font2.render('Score: ' + str(total_score), 1, (250, 255, 0))
            end_score = font2.render('if you want to restart the game press << Space >>',  1, (250, 255, 0))
            window.blit(end_score, (200, 395))
            window.blit(end_score2, (250, 350))
            pygame.display.update()
            continue

        window.blit(background, (0, 0))
        hero.update()
        hero.reset()
        Enemies.draw(window)
        Enemies.update()
        bullets.draw(window)
        bullets.update()
        gr_bonus.draw(window)
        gr_bonus.update()
        ye_bonus.draw(window)
        ye_bonus.update()
        meteorit.draw(window)
        meteorit.update()

        collides = pygame.sprite.groupcollide(Enemies, bullets, True, True)
        for i in collides:
            total_score += 1
            Enemies.add(Enemy('image/enemyship.png', random.randint(0, widght_win - wight_enemy) - 100, random.randint(0, 1000) * -1, random.randint(3, 5), wight_enemy, wight_enemy))

        if pygame.sprite.spritecollide(hero, Enemies, True):
            stop_game = True

        pygame.display.update()
        clock.tick(FPS)

init_db()

Enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
gr_bonus = pygame.sprite.Group()
ye_bonus = pygame.sprite.Group()
meteorit = pygame.sprite.Group()

pygame.mixer.init()
pygame.mixer.music.load('image/voice_space.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

fire_sound = pygame.mixer.Sound('image/shotgun.ogg')
fire_sound.set_volume(0.1)

registration_window()

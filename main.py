import pygame
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox
import time

# Инициализация базы данных
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY,
            username TEXT,
            time REAL
        )
    ''')
    conn.commit()
    conn.close()

# Регистрация пользователя
def register_user(username, password):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        open_main_menu(username)  # Открываем главное меню после успешной регистрации
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    conn.close()

# Вход пользователя
def login_user(username, password):
    global current_username
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        current_username = username  # Сохраняем имя пользователя
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        login_window.destroy()  # Закрываем окно входа
        open_main_menu(username)  # Открываем главное меню после успешного входа
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
        registration_window()  # Возвращаем на окно регистрации

# Окно главного меню
def open_main_menu(username):
    global main_menu
    main_menu = tk.Tk()
    main_menu.title("Главное меню")
    main_menu.geometry("400x400")

    tk.Label(main_menu, text=f"Добро пожаловать, {username}!").pack(pady=10)

    tk.Button(main_menu, text="Запустить игру", command=lambda: [main_menu.withdraw(), open_game_window()]).pack(pady=10)
    tk.Button(main_menu, text="Таблица лидеров", command=lambda: [main_menu.withdraw(), show_leaderboard()]).pack(pady=10)
    tk.Button(main_menu, text="Выйти из аккаунта", command=lambda: [main_menu.withdraw(), registration_window()]).pack(pady=10)

    main_menu.mainloop()

# Окно регистрации
def registration_window():
    global reg_window
    reg_window = tk.Tk()
    reg_window.title("Регистрация")
    reg_window.geometry("400x400")

    tk.Label(reg_window, text="Имя пользователя").pack(pady=10)
    username_entry = tk.Entry(reg_window)
    username_entry.pack(pady=5)

    tk.Label(reg_window, text="Пароль").pack(pady=10)
    password_entry = tk.Entry(reg_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(reg_window, text="Зарегистрироваться",
              command=lambda: register_user(username_entry.get(), password_entry.get())).pack(pady=10)
    tk.Button(reg_window, text="Войти", command=lambda: [reg_window.withdraw(), open_login_window()]).pack(pady=10)

    reg_window.mainloop()

# Окно входа
def open_login_window():
    global login_window
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
              command=lambda: [login_window.withdraw(), registration_window()]).pack(pady=10)

    login_window.mainloop()

# Параметры игры
hight_win = 800
widght_win = 1200
widght_Gera = 40
wight_enemy = 70
total_score = 0
mod_fire = 1
Enemy_amount = 5
start_time = 0
current_username = ""
game_paused = False  # Переменная для отслеживания состояния игры

# Инициализация Pygame
pygame.init()
font1 = pygame.font.Font(None, 36)
font2 = pygame.font.SysFont('corbel', 30)

# Классы
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
    global total_score, start_time
    total_score = 0
    start_time = 0
    global mod_fire
    gr_bonus.empty()
    ye_bonus.empty()
    meteorit.empty()
    Enemies.empty()
    mod_fire = 1
    hero.change_im('image/spaceshatel.png')

# Функция для запуска игры
def open_game_window():
    global window, start_time
    window = pygame.display.set_mode((widght_win, hight_win))
    pygame.display.set_caption("Звёздные войны")
    start_time = time.time()  # Запускаем таймер
    run_game()

# Основная логика игры
def run_game():
    global total_score, mod_fire, stop_game, game_paused
    total_score = 0
    mod_fire = 1
    stop_game = False
    game_paused = False  # Сброс состояния паузы

    # Создание спрайтов и групп
    global hero
    hero = player('image/spaceshatel.png', 370, 600, 5, 100, 150)
    for i in range(5):
        Enemies.add(Enemy('image/enemyship.png', random.randint(0, widght_win - wight_enemy) - 100, random.randint(0,  1000) * -1, random.randint(3, 5), wight_enemy, wight_enemy))

    clock = pygame.time.Clock()
    FPS = 60
    background = pygame.transform.scale(pygame.image.load("image/background.png"), (widght_win, hight_win))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and game_paused:
                    game_paused = False  # Возвращаем игру в активное состояние
                    run_game()  # Перезапускаем игру

        if stop_game:
            end_time = time.time() - start_time
            end_score2 = font2.render('Score: ' + str(total_score), 1, (250, 255, 0))
            end_time_text = font2.render(f'Time: {end_time:.2f} seconds', 1, (250, 255, 0))
            end_score = font2.render('Press << Space >> to return to menu',  1, (250, 255, 0))
            window.blit(end_score, (200, 395))
            window.blit(end_score2, (250, 350))
            window.blit(end_time_text, (250, 320))
            pygame.display.update()
            continue

        if game_paused:
            continue  # Игровой цикл приостановлен

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

        # Проверка на столкновение
        collides = pygame.sprite.groupcollide(Enemies, bullets, True, True)
        for i in collides:
            total_score += 1
            Enemies.add(Enemy('image/enemyship.png', random.randint(0, widght_win - wight_enemy) - 100, random.randint(0, 1000) * -1, random.randint(3, 5), wight_enemy, wight_enemy))

        if pygame.sprite.spritecollide(hero, Enemies, True) or pygame.sprite.spritecollide(hero, meteorit, True):
            stop_game = True
            game_paused = True  # Устанавливаем игру в состояние паузы
            save_leaderboard(total_score, time.time() - start_time)  # Сохраняем в таблицу лидеров

        # Обновление экрана
        pygame.display.update()
        clock.tick(FPS)

def save_leaderboard(score, time_taken):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leaderboard (username, time) VALUES (?, ?)', (current_username, time_taken))
    conn.commit()
    conn.close()

def show_leaderboard():
    leaderboard_window = tk.Tk()
    leaderboard_window.title("Таблица лидеров")
    leaderboard_window.geometry("400x400")

    tk.Label(leaderboard_window, text="Таблица лидеров").pack(pady=10)

    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, time FROM leaderboard ORDER BY time ASC')
    rows = cursor.fetchall()
    conn.close()

    for idx, (username, time) in enumerate(rows):
        tk.Label(leaderboard_window, text=f"{idx + 1}. {username} - {time:.2f} seconds").pack()

    tk.Button(leaderboard_window, text="Назад", command=lambda: [leaderboard_window.destroy(), main_menu.deiconify()]).pack(pady=10)

    leaderboard_window.mainloop()

# Инициализация Pygame и базы данных
init_db()

# Создание групп спрайтов
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

# Запуск окна регистрации
registration_window()
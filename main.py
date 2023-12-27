import pygame
import random
import math
from pygame import mixer
import time
import config

WIDTH = 800
HEIGHT = 600

player = type('Player', (), {})()
bullet = type('Bullet', (), {})()
enemies = []
lasers = []

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders OOP by Lucifer")
window_icon = pygame.image.load("alien.png")
pygame.display.set_icon(window_icon)

background_img = pygame.image.load("background.png")
background_music_paths = ["res/sounds/Space_Invaders_Music.ogg",
                          "res/sounds/Space_Invaders_Music_x2.ogg",
                          "res/sounds/Space_Invaders_Music_x4.ogg",
                          "res/sounds/Space_Invaders_Music_x8.ogg",
                          "res/sounds/Space_Invaders_Music_x16.ogg",
                          "res/sounds/Space_Invaders_Music_x32.ogg"]


def init_background_music():
    if config.difficulty == 1:
        mixer.quit()
        mixer.init()
    if config.difficulty <= 6:
        mixer.music.load(background_music_paths[config.difficulty - 1])
    else:
        mixer.music.load(background_music_paths[5])
    mixer.music.play(-1)


class Player:
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))


class Bullet:
    def __init__(self, img_path, width, height, x, y, dx, dy, fire_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fired = False
        self.fire_sound_path = fire_sound_path
        self.fire_sound = mixer.Sound(self.fire_sound_path)

    def draw(self):
        if self.fired:
            window.blit(self.img, (self.x, self.y))


class Laser:
    def __init__(self, img_path, width, height, x, y, dx, dy, shoot_probability, relaxation_time, beam_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.beamed = False
        self.shoot_probability = shoot_probability
        self.shoot_timer = 0
        self.relaxation_time = relaxation_time
        self.beam_sound_path = beam_sound_path
        self.beam_sound = mixer.Sound(self.beam_sound_path)

    def draw(self):
        if self.beamed:
            window.blit(self.img, (self.x, self.y))


def scoreboard():
    x_offset = 10
    y_offset = 10

    font = pygame.font.SysFont("калибр", 16)

    score_sprint = font.render("СЧет : " + str(config.score), True, (255, 255, 255))
    highest_score_sprint = font.render("Максимальный счет: " + str(config.highest_score), True, (255, 255, 255))
    level_sprint = font.render("Уровень : " + str(config.level), True, (255, 255, 255))
    difficulty_sprint = font.render("Сложность : " + str(config.difficulty), True, (255, 255, 255))
    life_sprint = font.render("Жизней : " + str(config.life) + " | " + ("@ " * config.life), True, (255, 255, 255))

    fps_sprint = font.render("FPS : " + str(config.fps), True, (255, 255, 255))
    frame_time_in_ms = round(config.single_frame_rendering_time * 1000, 2)
    frame_time_sprint = font.render("FT : " + str(frame_time_in_ms) + " ms", True, (255, 255, 255))

    window.blit(score_sprint, (x_offset, y_offset))
    window.blit(highest_score_sprint, (x_offset, y_offset + 20))
    window.blit(level_sprint, (x_offset, y_offset + 40))
    window.blit(difficulty_sprint, (x_offset, y_offset + 60))
    window.blit(life_sprint, (x_offset, y_offset + 80))
    window.blit(fps_sprint, (WIDTH - 80, y_offset))
    window.blit(frame_time_sprint, (WIDTH - 80, y_offset + 20))


def collision_check(object1, object2):
    x1_cm = object1.x + object1.width / 2
    y1_cm = object1.y + object1.width / 2
    x2_cm = object2.x + object2.width / 2
    y2_cm = object2.y + object2.width / 2
    distance = math.sqrt(math.pow((x2_cm - x1_cm), 2) + math.pow((y2_cm - y1_cm), 2))
    return distance < ((object1.width + object2.width) / 2)


def level_up():
    global life
    global level
    global difficulty
    global max_difficulty_to_level_up
    level_up_sound.play()
    config.level += 1
    config.life += 1
    config.difficulty = 1
    if config.level % 3 == 0:
        player.dx += 1
        bullet.dy += 1
        max_difficulty_to_level_up += 1
        for each_laser in lasers:
            each_laser.shoot_probability += 0.1
            if each_laser.shoot_probability > 1.0:
                each_laser.shoot_probability = 1.0
    if config.max_difficulty_to_level_up > 7:
        config.max_difficulty_to_level_up = 7

    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("Повышение уровня", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 120, HEIGHT / 2 - 32))
    pygame.display.update()
    init_game()
    time.sleep(1.0)


def respawn(enemy_obj):
    enemy_obj.x = random.randint(0, (WIDTH - enemy_obj.width))
    enemy_obj.y = random.randint(((HEIGHT / 10) * 1 - (enemy_obj.height / 2)),
                                 ((HEIGHT / 10) * 4 - (enemy_obj.height / 2)))


def kill_enemy(player_obj, bullet_obj, enemy_obj):
    global score
    global kills
    global difficulty
    bullet_obj.fired = False
    enemy_obj.kill_sound.play()
    bullet_obj.x = player_obj.x + player_obj.width / 2 - bullet_obj.width / 2
    bullet_obj.y = player_obj.y + bullet_obj.height / 2
    config.score = config.score + 10 * config.difficulty * config.level
    config.kills += 1
    if config.kills % config.max_kills_to_difficulty_up == 0:
        config.difficulty += 1
        if (config.difficulty == config.max_difficulty_to_level_up) and (config.life != 0):
            level_up()
        init_background_music()
    print("Счет:", config.score)
    print("Уровень:", config.level)
    print("Сложность:", config.difficulty)
    respawn(enemy_obj)


def rebirth(player_obj):
    player_obj.x = (WIDTH / 2) - (player_obj.width / 2)
    player_obj.y = (HEIGHT / 10) * 9 - (player_obj.height / 2)


def gameover_screen():
    scoreboard()
    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("GAME OVER", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 140, HEIGHT / 2 - 32))
    pygame.display.update()

    mixer.music.stop()
    game_over_sound.play()
    time.sleep(13.0)
    mixer.quit()


def gameover():
    global running
    global score
    global highest_score

    if config.score > config.highest_score:
        config.highest_score = config.score

    print("----------------")
    print("ИГРА ЗАКОНЧЕНА !!")
    print("\nВы умерли на")
    print("Уровень:", config.level)
    print("Сложность:", config.difficulty)
    print("Ваш результат:", config.score)
    print("\nПробовать снова !!")
    print("----------------")
    config.running = False
    gameover_screen()


def kill_player(player_obj, enemy_obj, laser_obj):
    global life
    laser_obj.beamed = False
    player_obj.kill_sound.play()
    laser_obj.x = enemy_obj.x + enemy_obj.width / 2 - laser_obj.width / 2
    laser_obj.y = enemy_obj.y + laser_obj.height / 2
    config.life -= 1
    print("Life Left:", config.life)
    if config.life > 0:
        rebirth(player_obj)
    else:
        gameover()


def destroy_weapons(player_obj, bullet_obj, enemy_obj, laser_obj):
    bullet_obj.fired = False
    laser_obj.beamed = False
    weapon_annihilation_sound.play()
    bullet_obj.x = player_obj.x + player_obj.width / 2 - bullet_obj.width / 2
    bullet_obj.y = player_obj.y + bullet_obj.height / 2
    laser_obj.x = enemy_obj.x + enemy_obj.width / 2 - laser_obj.width / 2
    laser_obj.y = enemy_obj.y + laser_obj.height / 2


def pause_game():
    pause_sound.play()
    scoreboard()
    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("PAUSED", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 80, HEIGHT / 2 - 32))
    pygame.display.update()
    mixer.music.pause()


def init_game():
    global pause_sound
    global level_up_sound
    global game_over_sound
    global weapon_annihilation_sound

    pause_sound = mixer.Sound("pause.wav")
    level_up_sound = mixer.Sound("1up.wav")
    game_over_sound = mixer.Sound("gameover.wav")
    weapon_annihilation_sound = mixer.Sound("annihilation.wav")

    player_img_path = "res/images/spaceship.gif"  # 64 x 64 px image
    player_width = 64
    player_height = 64
    player_x = (WIDTH / 2) - (player_width / 2)
    player_y = (HEIGHT / 10) * 9 - (player_height / 2)
    player_dx = config.initial_player_velocity
    player_dy = 0
    player_kill_sound_path = "res/sounds/explosion.wav"

    global player
    player = Player(player_img_path, player_width, player_height, player_x, player_y, player_dx, player_dy,
                    player_kill_sound_path)

    bullet_img_path = "res/images/bullet.png"  # 32 x 32 px image
    bullet_width = 32
    bullet_height = 32
    bullet_x = player_x + player_width / 2 - bullet_width / 2
    bullet_y = player_y + bullet_height / 2
    bullet_dx = 0
    bullet_dy = config.weapon_shot_velocity
    bullet_fire_sound_path = "res/sounds/gunshot.wav"

    global bullet
    bullet = Bullet(bullet_img_path, bullet_width, bullet_height, bullet_x, bullet_y, bullet_dx, bullet_dy,
                    bullet_fire_sound_path)

    enemy_img_path = "res/images/enemy.png"
    enemy_width = 64
    enemy_height = 64
    enemy_dx = config.initial_enemy_velocity
    enemy_dy = (HEIGHT / 10) / 2
    enemy_kill_sound_path = "res/sounds/enemykill.wav"

    laser_img_path = "res/images/beam.png"
    laser_width = 24
    laser_height = 24
    laser_dx = 0
    laser_dy = config.weapon_shot_velocity
    shoot_probability = 0.3
    relaxation_time = 100
    laser_beam_sound_path = "res/sounds/laser.wav"

    global enemies
    global lasers

    enemies.clear()
    lasers.clear()

    for lev in range(config.level):
        enemy_x = random.randint(0, (WIDTH - enemy_width))
        enemy_y = random.randint(((HEIGHT / 10) * 1 - (enemy_height / 2)), ((HEIGHT / 10) * 4 - (enemy_height / 2)))
        laser_x = enemy_x + enemy_width / 2 - laser_width / 2
        laser_y = enemy_y + laser_height / 2

        enemy_obj = Enemy(enemy_img_path, enemy_width, enemy_height, enemy_x, enemy_y, enemy_dx, enemy_dy,
                          enemy_kill_sound_path)
        enemies.append(enemy_obj)

        laser_obj = Laser(laser_img_path, laser_width, laser_height, laser_x, laser_y, laser_dx, laser_dy,
                          shoot_probability, relaxation_time, laser_beam_sound_path)
        lasers.append(laser_obj)


init_game()
init_background_music()
runned_once = False

while config.running:

    start_time = time.time()

    window.fill((0, 0, 0))
    window.blit(background_img, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            config.running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                print("LOG: Left Arrow Key Pressed Down")
                config.LEFT_ARROW_KEY_PRESSED = 1

            if event.key == pygame.K_RIGHT:
                print("LOG: Right Arrow Key Pressed Down")
                config.RIGHT_ARROW_KEY_PRESSED = 1

            if event.key == pygame.K_UP:
                print("LOG: Up Arrow Key Pressed Down")
                config.UP_ARROW_KEY_PRESSED = 1

            if event.key == pygame.K_SPACE:
                print("LOG: Space Bar Pressed Down")
                SPACE_BAR_PRESSED = 1

            if event.key == pygame.K_RETURN:
                print("LOG: Enter Key Pressed Down")
                config.ENTER_KEY_PRESSED = 1
                config.pause_state += 1

            if event.key == pygame.K_ESCAPE:
                print("LOG: Escape Key Pressed Down")
                config.ESC_KEY_PRESSED = 1
                config.pause_state += 1

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                config.RIGHT_ARROW_KEY_PRESSED = 0

            if event.key == pygame.K_LEFT:
                config.LEFT_ARROW_KEY_PRESSED = 0

            if event.key == pygame.K_UP:
                config.UP_ARROW_KEY_PRESSED = 0

            if event.key == pygame.K_SPACE:
                config.SPACE_BAR_PRESSED = 0

            if event.key == pygame.K_RETURN:
                config.ENTER_KEY_PRESSED = 0

            if event.key == pygame.K_ESCAPE:
                config.ESC_KEY_PRESSED = 0

    if config.pause_state == 2:
        config.pause_state = 0
        runned_once = False
        mixer.music.unpause()
    if config.pause_state == 1:
        if not runned_once:
            runned_once = True
            pause_game()
        continue

    if config.RIGHT_ARROW_KEY_PRESSED:
        player.x += player.dx
    if config.LEFT_ARROW_KEY_PRESSED:
        player.x -= player.dx

    if (config.SPACE_BAR_PRESSED or config.UP_ARROW_KEY_PRESSED) and not bullet.fired:
        bullet.fired = True
        bullet.fire_sound.play()
        bullet.x = player.x + player.width / 2 - bullet.width / 2
        bullet.y = player.y + bullet.height / 2

    if bullet.fired:
        bullet.y -= bullet.dy

    for i in range(len(enemies)):

        if not lasers[i].beamed:
            lasers[i].shoot_timer += 1
            if lasers[i].shoot_timer == lasers[i].relaxation_time:
                lasers[i].shoot_timer = 0
                random_chance = random.randint(0, 100)
                if random_chance <= (lasers[i].shoot_probability * 100):
                    lasers[i].beamed = True
                    lasers[i].beam_sound.play()
                    lasers[i].x = enemies[i].x + enemies[i].width / 2 - lasers[i].width / 2
                    lasers[i].y = enemies[i].y + lasers[i].height / 2

        enemies[i].x += enemies[i].dx * float(2 ** (config.difficulty - 1))

        if lasers[i].beamed:
            lasers[i].y += lasers[i].dy

    for i in range(len(enemies)):
        bullet_enemy_collision = collision_check(bullet, enemies[i])
        if bullet_enemy_collision:
            kill_enemy(player, bullet, enemies[i])

    for i in range(len(lasers)):
        laser_player_collision = collision_check(lasers[i], player)
        if laser_player_collision:
            kill_player(player, enemies[i], lasers[i])

    for i in range(len(enemies)):
        enemy_player_collision = collision_check(enemies[i], player)
        if enemy_player_collision:
            kill_enemy(player, bullet, enemies[i])
            kill_player(player, enemies[i], lasers[i])

    for i in range(len(lasers)):
        bullet_laser_collision = collision_check(bullet, lasers[i])
        if bullet_laser_collision:
            destroy_weapons(player, bullet, enemies[i], lasers[i])

    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width

    for enemy in enemies:
        if enemy.x <= 0:
            enemy.dx = abs(enemy.dx) * 1
            enemy.y += enemy.dy
        if enemy.x >= WIDTH - enemy.width:
            enemy.dx = abs(enemy.dx) * -1
            enemy.y += enemy.dy

    if bullet.y < 0:
        bullet.fired = False
        bullet.x = player.x + player.width / 2 - bullet.width / 2
        bullet.y = player.y + bullet.height / 2

    for i in range(len(lasers)):
        if lasers[i].y > HEIGHT:
            lasers[i].beamed = False
            lasers[i].x = enemies[i].x + enemies[i].width / 2 - lasers[i].width / 2
            lasers[i].y = enemies[i].y + lasers[i].height / 2

    scoreboard()
    for laser in lasers:
        laser.draw()
    for enemy in enemies:
        enemy.draw()
    bullet.draw()
    player.draw()

    pygame.display.update()

    config.frame_count += 1
    end_time = time.time()
    config.single_frame_rendering_time = end_time - start_time

    config.total_time = config.total_time + config.single_frame_rendering_time
    if config.total_time >= 1.0:
        config.fps = config.frame_count
        config.frame_count = 0
        config.total_time = 0
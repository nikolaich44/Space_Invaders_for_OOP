import pygame
import sys
from hero import Hero
from pygame.sprite import Group
from bullet import Bullet
from enemies import Enemies

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Counter Strike 3")
    hero = Hero(screen)
    enemies.gr = Group()
    bullets = Group()

    enemies = Enemies(screen)
    enemies_width = enemies.rect.width
    number_enemies_x = int((800 - 2 * enemies_width) / enemies_width)

    enemies_height = enemies.rect.height
    number_enemies_y = int((800 -400 - 2 * enemies_height) / enemies_height)

    for i in range(number_enemies_y):
        for j in range(number_enemies_x):
            enemies = Enemies(screen)
            enemies.x = enemies_width + enemies_width * j
            enemies.y = enemies_height + enemies_height * i
            enemies.rect.x = enemies.x
            enemies.rect.y = enemies.y

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hero.move_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    hero.move_right = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.move_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.move_left = False

        hero.output()
        pygame.display.flip()
        hero.moving(screen)


        screen.fill(0)
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        hero.output()
        pygame.display.flip()

        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullet.remove(bullet)


start_game()
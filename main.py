import pygame
import sys
from hero import Hero
from pygame.sprite import Group
from bullet import Bullet

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    pygame.display.set_caption("Counter Strike 3")
    hero = Hero(screen)
    bullets = Group()

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
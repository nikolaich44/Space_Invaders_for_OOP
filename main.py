import pygame, controller
from hero import Hero
from pygame.sprite import Group
from stats import Stats

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 900))
    pygame.display.set_caption("Counter Strike 2")

    hero = Hero(screen)
    bullets = Group()
    # enemy = Enemy(screen)
    enemies = Group()

    controller.create_army(screen, enemies)

    stats = Stats()
    flag = True
    while flag:
        controller.events(screen, hero, bullets)
        hero.output()
        pygame.display.flip()
        hero.moving(screen)

        controller.update(screen, hero, enemies, bullets)
        controller.update_bullets(screen, enemies,bullets)
        controller.update_enemys(stats, screen, hero, enemies, bullets)

start_game()
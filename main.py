import pygame
import sys
from hero import Hero

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    pygame.display.set_caption("Counter Strike 3")
    hero = Hero(screen)

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hero.move_right = True
            elif event.type == pygame.KEYUP:
                if event.type == pygame.K_d:
                    hero.move_right = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.move_left = True
            elif event.type == pygame.KEYUP:
                if event.type == pygame.K_a:
                    hero.move_left = False
        hero.output()
        pygame.display.flip()

start_game()
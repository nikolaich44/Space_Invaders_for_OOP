import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, hero):
        super(Bullet,self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,5,10) #посл. 2 цифры ширина, длина
        self.color = 255,255,255
        self.rect.centerx = hero.rect.centerx
        self.rect.top = hero.rect.top
        self.speed = 4.4
        self.y = float(self.rect.y)

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update_bullet(self):
        self.y -= self.speed
        self.rect.y = self.y

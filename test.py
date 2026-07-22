import pygame
from sys import exit
import math

play = True
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 550))
        self.barrel_offset = pygame.Vector2(25,12)
        
    def follow_mouse(self,x ,y):
        #image rotation follows mouse movement
        m_pos = pygame.mouse.get_pos()

        x_dist = m_pos[0] - self.rect.centerx
        y_dist = -(m_pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        old_center = self.rect.center

        self.image = pygame.transform.rotate(self.original_image, self.angle - 180)
        self.rect = self.image.get_rect(center=old_center)

        self.barrel_pos = self.barrel_offset.rotate(-self.angle) + self.rect.center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, barrel_pos):
        super().__init__()
        self.image = pygame.image.load("Images/BULLET.png").convert_alpha()
        self.rect = self.image.get_rect(center= (barrel_pos))

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
player_group.add(Player(500, 200))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(player_group.sprite.barrel_pos)
            bullet_group.add(bullet)

    screen.fill("black")

    if play:
        player_group.sprite.follow_mouse(500, 550)
        bullet_group.draw(screen)
        player_group.draw(screen)

    pygame.display.update()
    clock.tick(60)


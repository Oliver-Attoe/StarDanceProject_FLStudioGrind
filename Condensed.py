import pygame
from sys import exit
import math
import pytmx
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

GRAVITY = 0.5
playing_state = "start"
x = 600
y = 550

tmx_data = load_pygame("Maps/place_holder_map.tmx")
tiles = []

def load_collision():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    tiles.append(
                        pygame.Rect(
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight,
                            tmx_data.tilewidth,
                            tmx_data.tileheight
                        )
                    )

def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    screen.blit(
                        tile,
                        (x * tmx_data.tilewidth,
                         y * tmx_data.tileheight)
                    )

load_collision()

bg_surface = pygame.image.load("Images/BG.png").convert()
floor_surface = pygame.image.load("Images/Floor.png").convert()
floor_rect = floor_surface.get_rect(midbottom = (600, 800))

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(self.rect.center)

        self.gravity_enabled = False

        self.angle = 0

        self.barrel_offset = pygame.Vector2(30,12)
        
        self.velocity = pygame.Vector2(0, 0)

       

    def follow_mouse(self):
        self.m_pos = pygame.mouse.get_pos()

        x_dist = self.m_pos[0] - self.rect.centerx
        y_dist = -(self.m_pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

           
    def barrel_position(self):
        rotated_offset = self.barrel_offset.rotate(-(self.angle))
        return pygame.Vector2(self.rect.center) + rotated_offset
    
    def recoil(self,velocity):
        self.velocity -= velocity

    def in_air_rotate(self):
        self.angle += 6


    def update(self):
        if self.gravity_enabled == True:
            self.velocity.y += GRAVITY

        self.image = pygame.transform.rotate(self.original_image, self.angle -180)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos.x += self.velocity.x
        self.rect.centerx = self.pos.x

        self.pos.y += self.velocity.y
        self.rect.centery = self.pos.y

        self.velocity.x *= 0.975





    def tile_collision(self):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions


    def get_tile_mask(self):
       self.colides = self.tile_collision()
       for tile in self.colides:
        mask = pygame.mask.Mask(tile.size, fill=True)

        mask_surface = mask.to_surface()

        screen.blit(mask_surface, tile.topleft)

    def mask_collision(self):
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, barrel_offset,angle):
        super().__init__()

        self.original_image = pygame.image.load("Images/BULLET.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=barrel_offset)
        self.angle = angle

        direction = pygame.Vector2(1,0).rotate(-angle)


        if direction.length() > 0:
            direction = direction.normalize()

        self.velocity = direction * 15

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle -180)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.centerx <= 0 or self.rect.centerx >= 1200:
            self.kill()

        if self.rect.centery <=0 or self.rect.centery >=800:
            self.kill()


player_group = pygame.sprite.GroupSingle()
player_group.add(Player(x, y))

bullet_group = pygame.sprite.Group()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:

                playing_state = "in_proggress"
                player_group.sprite.gravity_enabled = True
                barrel = player_group.sprite.barrel_position()

                bullet = Bullet(barrel, player_group.sprite.angle)
                bullet_group.add(bullet)

                player_group.sprite.recoil(bullet.velocity)

    screen.blit(bg_surface, (0,0))
    screen.blit(floor_surface,floor_rect)
    draw_map()
        
        

        
        

    if playing_state == "start":
        player_group.sprite.follow_mouse()

            

    if playing_state == "in_proggress":
        player_group.sprite.in_air_rotate()


    player_group.sprite.get_tile_mask()
    player_group.update()


    bullet_group.update()
    bullet_group.draw(screen)


      
    player_group.draw(screen)
    for tile in tiles:
        pygame.draw.rect(screen, (255, 0, 0), tile, 2)

    pygame.display.update()
    clock.tick(60)
    
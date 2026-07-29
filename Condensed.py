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
level = "1"

match level:
    case "1":
        map_file = "Maps/place_holder_map.tmx"

tmx_data = load_pygame(map_file)
tiles = []

def load_collision():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    
                        rect = pygame.Rect(
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight,
                            tmx_data.tilewidth,
                            tmx_data.tileheight
                        )

                        mask = pygame.mask.Mask(rect.size, fill=True)

                        tiles.append({"rect": rect, "mask": mask, "id": gid})
 
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

x = 600
y = 550


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

        self.barrel_offset = pygame.Vector2(35,10)
        
        self.velocity = pygame.Vector2(0, 0)

        self.rot_speed = 0

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
        self.angle += self.rot_speed

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 180)
                
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
        self.mask = pygame.mask.from_surface(self.image)

    def stop_spin(self):
        if self.has_hit == True:
            self.rot_speed = 0
        else:
            self.rot_speed = 10

    def tile_collision(self):
       
        collisions = []

        for tile in tiles:

            if self.rect.colliderect(tile["rect"]):

                offset = (
                    tile["rect"].x - self.rect.x,
                    tile["rect"].y - self.rect.y
                )

                if self.mask.overlap(tile["mask"], offset):
                    collisions.append(tile)
                    

        return collisions

    def collisions_y(self):

        for tile in self.tile_collision():

            if self.velocity.y > 0:  # falling
                while self.mask.overlap(
                    tile["mask"],
                    (
                        tile["rect"].x - self.rect.x,
                        tile["rect"].y - self.rect.y
                    )
                ):
                    self.pos.y -= 1
                    self.rect.centery = self.pos.y
                    self.has_hit = True

                    self.velocity.y = 0
                    

                    

            elif self.velocity.y < 0:  # hitting ceiling
                while self.mask.overlap(
                    tile["mask"],
                    (
                        tile["rect"].x - self.rect.x,
                        tile["rect"].y - self.rect.y
                    )
                ):
                    self.pos.y += 1
                    self.rect.centery = self.pos.y
                    self.has_hit = True

                    self.velocity.y = 0

    def collisions_x(self):
        for tile in self.tile_collision():

            if self.velocity.x > 0:  # moving right
                while self.mask.overlap(
                    tile["mask"],
                    (
                        tile["rect"].x - self.rect.x,
                        tile["rect"].y - self.rect.y
                    )
                ):
                    self.pos.x -= 1
                    self.rect.centerx = self.pos.x
                    self.has_hit = True

                    self.velocity.x = 0

            elif self.velocity.x < 0:  # moving left
                while self.mask.overlap(
                    tile["mask"],
                    (
                        tile["rect"].x - self.rect.x,
                        tile["rect"].y - self.rect.y
                    )
                ):
                    self.pos.x += 1
                    self.rect.centerx = self.pos.x
                    self.has_hit = True

                    self.velocity.x = 0 

    def update(self):

        self.has_hit = False

        self.barrel_position()

        if self.gravity_enabled == True:
            self.velocity.y += GRAVITY

        # horizontal movement
        self.pos.x += self.velocity.x
        self.rect.centerx = self.pos.x

        self.collisions_x()

        # vertical movement
        self.pos.y += self.velocity.y
        self.rect.centery = self.pos.y
        
        self.collisions_y()

        if not self.has_hit:
            self.in_air_rotate()


        self.rotate_image()

        self.velocity.x *= 0.975


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

        self.velocity = direction * 15 #was15

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle -180)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        for tile in tiles:
            if self.rect.colliderect(tile["rect"]):
                self.kill()

player_group = pygame.sprite.GroupSingle()
player_group.add(Player(x, y))

bullet_group = pygame.sprite.Group()

#Game loop
while True:
    #event loop only
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:


                
            if playing_state == "start":
                player_group.sprite.pos = pygame.Vector2(600, 550)
            
                player_group.sprite.velocity = pygame.Vector2(0, 0)
                player_group.sprite.gravity_enabled = False

            playing_state = "in_proggress"
            barrel = player_group.sprite.barrel_position()

            bullet = Bullet(barrel, player_group.sprite.angle)
            bullet_group.add(bullet)

            player_group.sprite.recoil(bullet.velocity)
            player_group.sprite.gravity_enabled = True

    screen.blit(bg_surface, (0,0))

    draw_map()

    player_group.update()
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    if playing_state == "start":
        player_group.sprite.follow_mouse()

    else:
        player_group.sprite.stop_spin()

    pygame.display.update()
    clock.tick(60)
    
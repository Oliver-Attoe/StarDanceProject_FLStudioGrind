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
    
        self.pos = pygame.Vector2(self.rect.center)

        self.gravity_enabled = False

        self.angle = 0

        self.barrel_offset = pygame.Vector2(35,10)
        
        self.velocity = pygame.Vector2(0, 0)

        self.rot_speed = 0

        self.local_polygon = [
            pygame.Vector2(-23, 18),  # 1
            pygame.Vector2(32, 18),   # 2
            pygame.Vector2(28, 6),    # 3
            pygame.Vector2(-5, 6),    # 4
            pygame.Vector2(-16, -20),    # 5
            pygame.Vector2(-32, -20),     # 6
            pygame.Vector2(-20, 6),    # 7
            pygame.Vector2(-29, 6),   # 8
            ]


    def follow_mouse(self):
        self.m_pos = pygame.mouse.get_pos()

        x_dist = self.m_pos[0] - self.rect.centerx
        y_dist = -(self.m_pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

    
    def retical_line(self):
    # line starts at barrel, ends at mouse location

        barrel = self.barrel_position()
        mouse = pygame.mouse.get_pos()

        dx = mouse[0] - barrel[0]
        dy = mouse[1] - barrel[1]

        hypotenuse_length = math.hypot(dx, dy)

        if hypotenuse_length == 0:
            return

        direction_x = dx / hypotenuse_length
        direction_y = dy / hypotenuse_length

        for c in range(0, int(hypotenuse_length), 15):
            hyp_x = barrel[0] + direction_x * c
            hyp_y = barrel[1] + direction_y * c

            pygame.draw.circle(screen, "white", (int(hyp_x), int(hyp_y)), 3)
            #pygame.draw.circle(screen, "red", barrel, 5)

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
            self.rot_speed = 7
   
    def level_complete(self):
            for tile in tiles:
                if tile["id"] == 2:
                    if self.rect.colliderect(tile["rect"]):
                        print("LEVEL COMPLETE!!!")

    def get_global_polygon(self):
        self.global_polygon = []

        for point in self.local_polygon:
            rotated = point.rotate(-self.angle)
            self.global_polygon.append(rotated + self.pos)


    def get_axes(self, global_polygon):

        axes = []

        for i in range(len(global_polygon)):

            p1 = pygame.Vector2(global_polygon[i])
            p2 = pygame.Vector2(global_polygon[(i + 1) % len(global_polygon)])

            edge = p2 - p1

            axis = pygame.Vector2(-edge.y, edge.x).normalize()

            axes.append(axis)

        return axes


    def get_projections(self, axis, global_polygon):

        projections = []

        for point in global_polygon:
            projections.append(pygame.Vector2(point).dot(axis))

        return min(projections), max(projections)


    def polygon_collision(self, poly1, poly2):

        axes = self.get_axes(poly1) + self.get_axes(poly2)

        smallest_overlap = float("inf")
        smallest_axis = None

        for axis in axes:

            min1, max1 = self.get_projections(axis, poly1)
            min2, max2 = self.get_projections(axis, poly2)

            overlap = min(max1, max2) - max(min1, min2)

            if overlap <= 0:
                return False, None

            if overlap < smallest_overlap:
                smallest_overlap = overlap
                smallest_axis = axis

        return True, (smallest_axis, smallest_overlap)


    def rect_to_poly(self, rect):

        return [
        pygame.Vector2(rect.topleft),
        pygame.Vector2(rect.topright),
        pygame.Vector2(rect.bottomright),
        pygame.Vector2(rect.bottomleft)
                ]


    def test_collision(self):

        for tile in tiles:

            tile_poly = self.rect_to_poly(tile["rect"])
            

            collided, response = self.polygon_collision(
                self.global_polygon,
                tile_poly
            )

            if collided:
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                pygame.draw.polygon(screen, "red", tile_poly, 2)

    

    def collision_x(self):

        for tile in tiles:
            if not self.rect.colliderect(tile["rect"]):
                continue
            tile_poly = self.rect_to_poly(tile["rect"])

            collided, response = self.polygon_collision(
                self.global_polygon,
                tile_poly
            )

            if collided:

                axis, overlap = response

                # only resolve horizontal collisions
                if abs(axis.x) > abs(axis.y):

                    if self.velocity.x > 0:
                        self.pos.x -= overlap
                    elif self.velocity.x < 0:
                        self.pos.x += overlap

                    self.velocity.x = 0

                    self.rect.center = self.pos
                    self.get_global_polygon()


    def collision_y(self):

        for tile in tiles:
            if not self.rect.colliderect(tile["rect"]):
                continue

            tile_poly = self.rect_to_poly(tile["rect"])

            collided, response = self.polygon_collision(
                self.global_polygon,
                tile_poly
            )

            if collided:

                axis, overlap = response

                # only resolve vertical collisions
                if abs(axis.y) > abs(axis.x):

                    if self.velocity.y > 0:
                        # falling onto floor
                        self.pos.y -= overlap

                    elif self.velocity.y < 0:
                        # hitting ceiling
                        self.pos.y += overlap


                    self.velocity.y = 0

                    self.rect.center = self.pos
                    self.get_global_polygon()

    def update(self):

   
        
        self.get_global_polygon()

        self.in_air_rotate()

        self.rotate_image()

        self.barrel_position()

        if self.gravity_enabled == True:
            self.velocity.y += GRAVITY

        steps = max(1, int(abs(self.velocity.x)))

        for _ in range(steps):
            self.pos.x += self.velocity.x / steps
            self.rect.centerx = self.pos.x

            self.get_global_polygon()
            self.collision_x()


        # vertical movement
        steps = max(1, int(abs(self.velocity.y)))

        for _ in range(steps):
            self.pos.y += self.velocity.y / steps
            self.rect.centery = self.pos.y

            self.get_global_polygon()
            self.collision_y()

        self.velocity.x *= 0.975
        self.level_complete()
        self.test_collision()

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
    
        if pygame.mouse.get_pressed()[0]:
            if game_state == "getting_hint":
                draw_signature(screen,signing)
                signing = True
        else:
            signing = False


    pygame.display.update()
    clock.tick(60)
    
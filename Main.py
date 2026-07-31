import pygame
from sys import exit
import math
import pytmx
from pytmx.util_pygame import load_pygame


pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

GRAVITY = 0.5
BOUNCE = 0.2
game_state = "start_menu"
playing_state = "start"
paused = False
level = "1"

match level:
    case "1":
        map_file = "Maps/place_holder_map.tmx"




button_fx = pygame.mixer.Sound("Sounds/button_pressed.mp3")
gun_fired_fx = pygame.mixer.Sound("Sounds/bullet_fired.mp3")
start_music = True




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

start_surface = pygame.image.load("Images/Start_screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (600, 125))
start_button  = pygame.image.load("Images/Button.png").convert()
start_button_rect = start_button.get_rect(center = (600,400))

#This section is sisplayed in playing game state
bg_surface = pygame.image.load("Images/BG.png").convert()

pause_surface = pygame.image.load("Images/Pause.png").convert()
pause_rect = pause_surface.get_rect(topleft = (1140, 0))
pause_menu = pygame.image.load("Images/Pause_menu.png")
pause_menu_rect = pause_menu.get_rect(center = (600, 400))
home_surface = pygame.image.load("Images/Home_button.png")
home_rect = home_surface.get_rect(center = (600, 400))
cont_surface = pygame.image.load("Images/continue_button.png")
cont_rect = cont_surface.get_rect(center = (700, 400))

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
        self.velocity -= velocity * 1.5

    def in_air_rotate(self):
        self.angle += self.rot_speed

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 180)
                
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
        self.mask = pygame.mask.from_surface(self.image)

    def start_spin(self):

        self.rot_speed = 10

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

        center1 = sum(poly1, pygame.Vector2()) / len(poly1)
        center2 = sum(poly2, pygame.Vector2()) / len(poly2)

        direction = center2 - center1

        if smallest_axis.dot(direction) < 0:
            smallest_axis = -smallest_axis

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
                pygame.draw.polygon(screen, "red", tile_poly, 2)

    def resolve_collisions(self):

        self.grounded = False
        self.celling_hit = False

        for tile in tiles:

            if not self.rect.colliderect(tile["rect"]):
                continue

            tile_poly = self.rect_to_poly(tile["rect"])

            collided, response = self.polygon_collision(
                self.global_polygon,
                tile_poly
            )

            if not collided:
                continue

            axis, overlap = response

            # Move the axis so it always points from the tile to the player
            tile_center = pygame.Vector2(tile["rect"].center)
            direction = self.pos - tile_center

            if axis.dot(direction) < 0:
                axis = -axis

            # Minimum Translation Vector
            mtv = axis * overlap

            # Push player out of tile
            self.pos += mtv

            self.rect.center = self.pos
            self.get_global_polygon()

            # Remove velocity into the surface
            vn = self.velocity.dot(axis)

            if vn < 0:
                self.velocity -= axis * vn

            # Ground / ceiling
            if axis.y < -0.7:
                self.grounded = True
                self.rot_speed = 0

            elif axis.y > 0.7:
                self.celling_hit = True
                self.rot_speed = 0

    def level_complete(self):
        for tile in tiles:
            if tile["id"] == 2:
                if self.rect.colliderect(tile["rect"]):
                    print("yres")

    #def restart(self):


    

    def update(self):

        self.barrel_position()

        self.celling_hit = False
        self.grounded = False
        if self.gravity_enabled == True:
            self.velocity.y += GRAVITY

        steps = max(1, int(abs(self.velocity.x)))

        for _ in range(steps):
            self.pos.x += self.velocity.x / steps
            self.rect.centerx = self.pos.x
            self.get_global_polygon()
            self.resolve_collisions()


        # vertical movement
        steps = max(1, int(abs(self.velocity.y)))

        for _ in range(steps):
            self.pos.y += self.velocity.y / steps
            self.rect.centery = self.pos.y
            self.get_global_polygon()
            self.resolve_collisions()

        self.get_global_polygon()
        self.in_air_rotate()

        if paused == False:
            self.rotate_image()

        self.velocity.x *= 0.985
        self.test_collision()
        self.level_complete()
        

        


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

        self.velocity = direction * 19 #was15

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
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_button_rect.collidepoint(event.pos) and game_state == "start_menu":
                button_fx.play()

                
                game_state = "playing"
                if paused == True:
                    paused = False
                    player_group.sprite.pos = pygame.Vector2(600, 550)
                    playing_state = "start"
                    player_group.sprite.velocity = pygame.Vector2(0, 0)
                    player_group.sprite.gravity_enabled = False

                

            elif game_state == "playing":
                if paused == False:
                    gun_fired_fx.play()
                    playing_state = "in_proggress"
                    barrel = player_group.sprite.barrel_position()

                

                    bullet = Bullet(barrel, player_group.sprite.angle)
                    bullet_group.add(bullet)

                    player_group.sprite.recoil(bullet.velocity)
                    player_group.sprite.gravity_enabled = True

                if pause_rect.collidepoint(event.pos):
                    paused = True

                if paused and home_rect.collidepoint(event.pos):
                    game_state = "start_menu"
                    start_music = True
                               


                if cont_rect.collidepoint(event.pos):
                    paused = False

                




    if game_state == "start_menu":
        
        screen.blit(start_surface, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(s_text, s_text_rect)
        if start_music == True:
            pygame.mixer.music.load("Sounds/human_music.mp3")
            pygame.mixer.music.play(-1)
            start_music = False
        
        


    elif game_state == "playing":

        if start_music == False:
            pygame.mixer.music.stop()

        screen.blit(bg_surface, (0,0))
        
        draw_map()

        screen.blit(pause_surface, pause_rect)




        if paused == False:
            player_group.update()
            


            bullet_group.update()
            bullet_group.draw(screen)


      
            player_group.draw(screen)
        
        

        
        

            if playing_state == "start":
                player_group.sprite.follow_mouse()
                player_group.sprite.retical_line()

            

            if playing_state == "in_proggress":
                player_group.sprite.start_spin()


        else:
            
            screen.blit(pause_menu, pause_menu_rect)
            screen.blit(home_surface, home_rect)
            screen.blit(cont_surface, cont_rect)
                
    
    pygame.display.update()
    clock.tick(60)
    
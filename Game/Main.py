import pygame
from sys import exit
import math
import pytmx
from pytmx.util_pygame import load_pygame
import Settings
from UI import *
from SOUNDS import *
import Timer


pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

level_selection = button_generation(Settings.levels)
map_file, start_x, start_y, bullet_count, bullet_max, goal_x, goal_y, m_stars, m_stars_required= Settings.level_load()
star, star_rect, star_polygon = create_star(goal_x, goal_y)
mini_stars_list = create_mini_stars()

timer = Timer.Stopwatch()

tmx_data = load_pygame(map_file)
tiles = []

def load_collision():

    tiles.clear()
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)
                properties = tmx_data.get_tile_properties_by_gid(gid)

                if tile:
                    
                        rect = pygame.Rect(
                            x * tmx_data.tilewidth,
                            y * tmx_data.tileheight,
                            tmx_data.tilewidth,
                            tmx_data.tileheight
                        )

                        mask = pygame.mask.Mask(rect.size, fill=True)

                        tiles.append({"rect": rect, "mask": mask, "property": properties})
                            
 
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

def load_level(map_file):
    global tmx_data

    tmx_data = load_pygame(map_file)

    tiles.clear()
    load_collision()

m_star_collected = False

load_level(map_file)

class Player(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
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

        self.global_polygon = []
        self.get_global_polygon()
        self.goal_progress = 0


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
        self.image = pygame.transform.rotate(
        self.original_image,
        self.angle - 180
        )

        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.get_global_polygon()

    def start_spin(self):

        self.rot_speed = 11

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

            #kill block function moved here
            if tile["property"].get("type") == "Kill":
                crash_fx.play()
                Settings.game_state = "lost"
                return


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
                self. velocity *= 0.96

            elif axis.y > 0.7:
                self.celling_hit = True
                self.rot_speed = 0

    def level_complete(self):
        collided, response = self.polygon_collision(
            self.global_polygon,
            star_polygon
        )

        if m_stars == True:
            if self.goal_progress >= m_stars_required:
                screen.blit(star, star_rect)
                if collided:
            
                    win_fx.play()
                    timer.stop()

            
                    Settings.game_state = "has_won"

        else:
            screen.blit(star, star_rect)
            if collided:
            
                win_fx.play()
                timer.stop()

            
                Settings.game_state = "has_won"


    def realign(self):
        a = pygame.key.get_pressed()
        if self.grounded:
            if a[pygame.K_a]:
                self.angle += 7
                self.velocity = pygame.Vector2(0, 0)


    def mini_star_load(self):

        if m_stars:
            for star in mini_stars_list:


                if star["collected"]:
                    continue
                    
                screen.blit(mini_star ,star["rect"])

                collided, response = self.polygon_collision(
                    self.global_polygon,
                    star["polygon"]
                )

                if collided:
                    star["collected"] = True
                    self.goal_progress += 1
                    print("collision detected:", self.goal_progress)
                
                        

                
                


        

    def update(self):
        
        self.barrel_position()

        self.celling_hit = False
        self.grounded = False
        if self.gravity_enabled == True:
            self.velocity.y += Settings.GRAVITY

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


        
        self.in_air_rotate()
        
        self.get_global_polygon()

        if Settings.paused == False:
            self.rotate_image()

        

        self.velocity.x *= 0.985
        self.test_collision()
        self.level_complete()
        self.realign()
        self.mini_star_load()



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
player_group.add(Player(start_x, start_y))

bullet_group = pygame.sprite.Group()


#Game loop
while True:
    #event loop only
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            match Settings.game_state:
                case "start_menu":
                    if start_button_rect.collidepoint(event.pos):
                        button_fx.play()
                
                        Settings.game_state = "playing"
                        Settings.playing_state = "start"
                

                    if Settings.paused == True:
                        Settings.paused = False
                        player_group.sprite.pos = pygame.Vector2(start_x, start_y)
                        Settings.playing_state = "start"
                        player_group.sprite.velocity = pygame.Vector2(0, 0)


                    if level_button_rect2.collidepoint(event.pos):
                        Settings.game_state = "selecting_level"
                    
            
                case"playing":
                    if Settings.paused == False:
                        barrel = player_group.sprite.barrel_position()
                        if bullet_count < bullet_max:
                            bullet = Bullet(barrel, player_group.sprite.angle)
                            bullet_group.add(bullet)
                            bullet_count += 1
                            gun_fired_fx.play()
                            player_group.sprite.recoil(bullet.velocity)
                            player_group.sprite.gravity_enabled = True
                            if Settings.playing_state == "start":
                                timer.start()
                                Settings.playing_state = "in_proggress"

                    if pause_rect.collidepoint(event.pos):
                        Settings.paused = True
                        timer.pause()

                    if Settings.paused and home_rect.collidepoint(event.pos):
                        Settings.game_state = "start_menu"
                        start_music = True
                               
                    if cont_rect.collidepoint(event.pos):
                        Settings.paused = False
                        timer.resume()

                    if level_button_rect.collidepoint(event.pos):
                        Settings.game_state = "selecting_level"




                case "selecting_level":
                    for button in level_selection:

                        if button.rect.collidepoint(event.pos):

                            current_level = button.level
                            Settings.player_level = current_level
                        

                            map_file, start_x, start_y, bullet_count, bullet_max, goal_x, goal_y, m_stars, m_stars_required = Settings.level_load()
                            star, star_rect, star_polygon = create_star(goal_x, goal_y)
                            mini_stars_list = create_mini_stars()


                            load_level(map_file)
                        

                            
                            Settings.game_state = "playing"
                            Settings.playing_state = "start"
                            Settings.paused = False


                case "lost":
                    if restart_button_rect.collidepoint(event.pos):
                        Settings.playing_state = "start"
                        Settings.game_state = "playing"

                        player_group.sprite.pos = pygame.Vector2(start_x, start_y)
                        player_group.sprite.velocity = pygame.Vector2(0, 0)
                        player_group.sprite.gravity_enabled = False

                    continue

                case "has_won":
                    if next_level_rect.collidepoint(event.pos):#
                        Settings.player_level += 1
                        Settings.playing_state = "start"
                        Settings.game_state = "playing"

                        map_file, start_x, start_y, bullet_count, bullet_max, goal_x, goal_y, m_stars, m_stars_required = Settings.level_load()
                        star, star_rect, star_polygon = create_star(goal_x, goal_y)
                        mini_stars_list = create_mini_stars()

                        load_level(map_file)

                        player_group.sprite.pos = pygame.Vector2(start_x, start_y)
                        player_group.sprite.velocity = pygame.Vector2(0, 0)
                        player_group.sprite.gravity_enabled = False


                    continue                        


#Non-events below
###############################################

    match Settings.game_state:
        case "start_menu":
            Settings.paused = False
            screen.blit(start_surface, (0,0))
            screen.blit(start_button, start_button_rect)
            screen.blit(s_text, s_text_rect)
            screen.blit(level_button, level_button_rect2)
            if start_music == True:
                play_music()
                start_music = False

        
        case "playing":

            if start_music == False:
                pygame.mixer.music.stop()



            screen.blit(bg_surface, (0,0))
            
           
            
        
            draw_map()

            screen.blit(pause_surface, pause_rect)


            if Settings.paused == False:
                player_group.update()
                player_group.sprite.gravity_enabled = False
                bullet_group.update()
                timer.update()


            bullet_group.draw(screen)
            player_group.draw(screen)
            timer.display_timer(screen)
        
            match Settings.playing_state:
                case "start":
                    player_group.sprite.rot_speed = 0
                    player_group.sprite.follow_mouse()
                    player_group.sprite.retical_line()
                    player_group.sprite.rect.centerx = start_x
                    player_group.sprite.rect.centery = start_y
                    player_group.sprite.pos = pygame.Vector2(player_group.sprite.rect.center)
                    player_group.sprite.velocity =  pygame.Vector2(0,0)
                    m_star_collected = False
                
                    bullet_count = 0
                    timer.reset_time()

                case "in_proggress":
                    player_group.sprite.start_spin()

                    r = pygame.key.get_pressed()
                    player_group.sprite.gravity_enabled = True
                    if r[pygame.K_r]:
                        Settings.time += 1
                        if Settings.time >= 120:
                            Settings.playing_state = "start"
                            Settings.time = 0
                            timer.reset_time()
                            m_star_collected = False




        case "lost":
            screen.blit(loss_screen, loss_screen_rect)
            screen.blit(restart_button, restart_button_rect)


        case "has_won":
            screen.blit(win_screen, win_screen_rect)
            screen.blit(next_level,next_level_rect)
            timer.display_timer(screen)
            
            

        
        case "selecting_level":
            Settings.paused = False
            screen.blit(level_select_BG, (0,0))
            level_selection.draw(screen)

    
    if Settings.paused:
            
        screen.blit(pause_menu, pause_menu_rect)
        screen.blit(home_surface, home_rect)
        screen.blit(cont_surface, cont_rect)
        screen.blit(level_button, level_button_rect)

    #print(pygame.mouse.get_pos())
    
    #pygame.draw.rect(screen, (255,0,0), player_group.sprite.rect, 2)
    #pygame.draw.polygon(screen, (0,255,0), player_group.sprite.global_polygon, 2)
    pygame.display.update()
    clock.tick(60)
    
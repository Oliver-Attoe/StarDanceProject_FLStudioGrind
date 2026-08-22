import pygame
from sys import exit
import math
import Settings
from UI import *
from SOUNDS import *
import Timer
import Tiles
import random
import Waiver
import Dialogue
#Imports ONLY
###############################################################################################################

pygame.init()
screen = pygame.display.set_mode((1200, 800))
game_clock = pygame.time.Clock()

level_selection = button_generation(Settings.levels)
gun_selection = gun_button_generation()
check_boxes = Waiver.check_box_generation(screen, unchecked_box)
map_file, start_x, start_y, bullet_max, goal_x, goal_y, m_stars, m_stars_required, kill_is_req, kills_req, bonus_time= Settings.level_load()
star, star_rect, star_polygon = create_star(goal_x, goal_y)
mini_stars_list = create_mini_stars()
dialogue = Dialogue.Dialogue()


timer = Timer.Stopwatch()

m_star_collected = False

Tiles.load_level(map_file)

#Class's ONLY
#################################################################################################################
class Player(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y):
        super().__init__()
        gun_image = Settings.set_gun_image()

        self.original_image = pygame.image.load(f"Images/{gun_image}").convert_alpha()

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


        self.portal_cooldown = 0

        self.frozen = False

        self.kill_count = 0

        self.rotation_direction = 1

        self.gravity_flip = 1

        self.tp_enabled = False

        self.ghost_enabled = False


    def follow_mouse(self):
        if Dialogue.dialogue_active[Settings.player_level - 1][0] == False:
            self.m_pos = pygame.mouse.get_pos()

            x_dist = self.m_pos[0] - self.rect.centerx
            y_dist = -(self.m_pos[1] - self.rect.centery)

            self.angle = math.degrees(math.atan2(y_dist, x_dist))

    def retical_line(self):
        if Dialogue.dialogue_active[Settings.player_level - 1][0] == False:

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
        self.angle += self.rot_speed * Settings.time_multiplyer

    def rotate_image(self):
        self.image = pygame.transform.rotate(
        self.original_image,
        self.angle - 180
        )

        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.get_global_polygon()

    def start_spin(self):

        self.rot_speed = 11 * self.rotation_direction

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

    def resolve_collisions(self):

        self.grounded = False
        self.celling_hit = False
        near_tiles = []

        for tile in Tiles.tiles:

            tile_type = tile["property"].get("type")

            if tile_type in Tiles.open_gates:
                continue

            if tile_type in Tiles.broken_tiles:
                continue

            if self.rect.colliderect(tile["rect"]):
                near_tiles.append(tile)


        for tile in near_tiles:
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

            if tile["property"].get("type") == "Blue":
                return

            if tile["property"].get("type") == "Orange":
                return






            

            axis, overlap = response

            #Move the axis so it always points from the tile to the player
            tile_center = pygame.Vector2(tile["rect"].center)
            direction = self.pos - tile_center

            if axis.dot(direction) < 0:
                axis = -axis

            #Minimum Translation Vector
            mtv = axis * overlap

            #Push player out of tile
            self.pos += mtv

            self.rect.center = self.pos
            self.get_global_polygon()

            #Remove velocity into surface
            vn = self.velocity.dot(axis)

            if vn < 0:
                self.velocity -= axis * vn

            #Ground / ceiling
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

        elif kill_is_req == True:
            if Settings.kill_count >= kills_req:
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

        if self.gravity_flip == 1:
            if self.grounded and a[pygame.K_a]:

                if self.rotation_direction > 0:
                    self.angle += 7
                else:
                    self.angle -= 7

                self.velocity = pygame.Vector2(0, 0)

        else:
            if self.celling_hit and a[pygame.K_a]:

                if self.rotation_direction > 0:
                    self.angle += 7
                else:
                    self.angle -= 7

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

    def portal_collision(self):

        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1
        
        for portal in Tiles.portals:
            if self.portal_cooldown <= 0:
                if self.rect.colliderect(portal["rect"]):
                

                    destination = next(
                        p for p in Tiles.portals
                        if p["portal_id"] == portal["portal_target"]
                    )

                    entry_angle = portal["portal_rotation"]
                    exit_angle = destination["portal_rotation"]

                    if self.angle > 0:
                        rotation_difference = entry_angle - exit_angle
                    else:
                        rotation_difference = -(entry_angle - exit_angle)
                    self.velocity.rotate_ip(rotation_difference)
                    self.pos = pygame.Vector2(destination["rect"].center)
                    self.portal_cooldown = 30

    def clock_image_load(self):
        for clock in Tiles.abilities:
            if clock["ability_type"] != "clock":
                continue

            if clock["collected"]:
                continue

            screen.blit(clock_surafce,clock["rect"])

    def time_stop_ability(self):
        for clock in Tiles.abilities:
            if clock["ability_type"] != "clock":
                continue

            if clock["collected"]:
                continue
            
            if self.rect.colliderect(clock["rect"]):
                clock["collected"] = True
                self.frozen = True            

    def frozen_update(self):

        self.barrel_position()
        self.follow_mouse()
        self.retical_line()
        self.velocity = pygame.Vector2(0,0)
        self.rotate_image()
        self.rot_speed =  0

    def reset_player(self):

        self.pos = pygame.Vector2(start_x, start_y)
        self.rect.center = (start_x, start_y)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity_enabled = False
        self.frozen = False
        self.rot_speed = 0
        self.goal_progress = 0
        self.gravity_flip =  1
        self.tp_enabled = False
        self.ghost_enabled = False

    def kill_bad_guys(self):
        
        for obj in Tiles.bad_guys:

            if obj["killed"]:
                continue

            if self.rect.colliderect(obj["rect"]):
                obj["killed"] = True
                Settings.kill_count += 1

    def load_buttons(self):

        for button in Tiles.buttons:

           
            if button["pressed"]:
                continue

            
            if button["name"] == "purple_button":
                screen.blit(purple_button, button["rect"])

            elif button["name"] == "green_button":
                screen.blit(green_button, button["rect"])

            elif button["name"] == "white_button":
                screen.blit(white_button, button["rect"])

    def button_detection_gun(self):

        for button in Tiles.buttons:

            if button["pressed"]:
                continue
            
            if self.rect.colliderect(button["rect"]):

                if button["name"] == "green_button":
                    Tiles.open_gates.add("Green")
                    button["pressed"] = True

                elif button["name"] == "white_button":
                    Tiles.open_gates.add("White")
                    button["pressed"] = True         

    def change_gun(self):

        gun_image = Settings.set_gun_image()

        self.original_image = pygame.image.load(f"Images/{gun_image}").convert_alpha()

        self.image = self.original_image

    def load_room(self):
        if random.random() < 0.02:
            man_ogg.stop()
            Settings.player_level = 0
            man_ogg.play(-1)
            Settings.gun = 0
            self.change_gun()
        else:
            man_ogg.stop()

    def rotation_reverse(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "reverse_rotation":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True

                self.rotation_direction *= -1
                self.rot_speed = 11 * self.rotation_direction     

    def rotation_load(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "reverse_rotation":
                continue

            if ability["collected"]:
                continue

            screen.blit(rotation_arrow,ability["rect"])

    def bullet_pickup(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "bullet_pickup":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True

                Settings.bullet_count -= 1

    def bullet_pickup_load(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "bullet_pickup":
                continue

            if ability["collected"]:
                continue

            screen.blit(bullet_pickup_surface,ability["rect"])
   
    def slow_time(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "slow_time":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True
                Settings.time_multiplyer = 0.4
                Settings.slow_time_active = True
                Settings.slow_time_start = pygame.time.get_ticks()

    def slow_time_load(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "slow_time":
                continue

            if ability["collected"]:
                continue

            screen.blit(slow_time_surface,ability["rect"])   

    def gravity_swap(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "gravity_swap":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True
                self.gravity_flip = -1

    def gravity_swap_load(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "gravity_swap":
                continue

            if ability["collected"]:
                continue

            screen.blit(gravity_swap_surface,ability["rect"])   

        
    def bonus_time_star(self):

        if Settings.level_stars[Settings.player_level - 1][0] == True:
            return

        if (timer.time_passed / 1000) <= bonus_time:
            Settings.total_stars += 1
            Settings.level_stars[Settings.player_level - 1][0] = True

    def normal_star(self):
        if Settings.level_stars[Settings.player_level - 1][1] == True:
            return

        if self.polygon_collision(self.global_polygon, star_polygon):
            Settings.total_stars += 1
            Settings.level_stars[Settings.player_level - 1][1] = True

    def bonus_bullet_star(self):
        if Settings.level_stars[Settings.player_level - 1][2] == True:
            return

        if Settings.bullet_count < bullet_max:
            Settings.total_stars += 1
            Settings.level_stars[Settings.player_level - 1][2] = True

    def level_start_dialogue(self):
        if Dialogue.dialogue_active[Settings.player_level - 1][0] == False:
            return False

        if Dialogue.dialogue_active[Settings.player_level - 1][0] == True:
            Dialogue.dialogue_active[Settings.player_level - 1][0] = False
            return True

    def level_won_dialogue(self):
        if Dialogue.dialogue_active[Settings.player_level - 1][1] == False:
            return False

        if Dialogue.dialogue_active[Settings.player_level - 1][1] == True:
            Dialogue.dialogue_active[Settings.player_level - 1][1] = False
            return True
        
            



        
            

    def tp_bullet_ability(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "tp_bullet":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True

                Settings.bullet_count -= 1
                self.tp_enabled = True

    def load_tp_bullet(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "tp_bullet":
                continue

            if ability["collected"]:
                continue

            screen.blit(tp_bullet,ability["rect"])  

    def ghost_bullet(self):
        for ability in Tiles.abilities:

            if ability["ability_type"] != "ghost_bullet":
                continue

            if ability["collected"]:
                continue

            if self.rect.colliderect(ability["rect"]):
                ability["collected"] = True
                self.ghost_enabled = True

    def ghost_bullet_load(self):
        for ability in Tiles.abilities:
            if ability["ability_type"] != "ghost_bullet":
                continue

            if ability["collected"]:
                continue

            screen.blit(ghost_bullet,ability["rect"]) 


        

    def update(self):

        self.celling_hit = False
        self.grounded = False
        if self.gravity_enabled == True:
            self.velocity.y += Settings.GRAVITY * Settings.time_multiplyer * self.gravity_flip

        steps = max(1, int(abs(self.velocity.x)))

        for _ in range(steps):
            self.pos.x += (self.velocity.x * Settings.time_multiplyer) / steps
            self.rect.centerx = self.pos.x
            self.get_global_polygon()
            self.resolve_collisions()
           


        #vertical movement
        steps = max(1, int(abs(self.velocity.y)))

        for _ in range(steps):
            self.pos.y += (self.velocity.y * Settings.time_multiplyer) / steps
            self.rect.centery = self.pos.y
            self.get_global_polygon()
            self.resolve_collisions()


        
        self.in_air_rotate()
        
        self.get_global_polygon()

        if Settings.paused == False:
            self.rotate_image()

        

        self.velocity.x *= 0.985
        self.realign()
        self.portal_collision()

        self.time_stop_ability()
        self.kill_bad_guys()
        self.button_detection_gun()
        self.rotation_reverse()
        self.bullet_pickup()
        self.slow_time()
        self.gravity_swap()
        self.tp_bullet_ability()
        self.ghost_bullet()
        




class Bullet(pygame.sprite.Sprite):
    def __init__(self, barrel_offset,angle,player):
        super().__init__()

        self.original_image = pygame.image.load("Images/BULLET.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=barrel_offset)
        self.angle = angle

        direction = pygame.Vector2(1,0).rotate(-angle)


        if direction.length() > 0:
            direction = direction.normalize()

        self.velocity = direction * 19 #was15

        self.player = player


        self.ghost = player.ghost_enabled

        if player.ghost_enabled:
            player.ghost_enabled = False

    def kill_bad_guys(self):
        
        for obj in Tiles.bad_guys:

            if obj["killed"]:
                continue

            if self.rect.colliderect(obj["rect"]):
                obj["killed"] = True
                Settings.kill_count += 1

    def button_detection_bullets(self):

        for button in Tiles.buttons:

           
            if button["pressed"]:
                continue

            
            if self.rect.colliderect(button["rect"]):

                if button["name"] == "purple_button":
                    Tiles.open_gates.add("Purple")
                    button["pressed"] = True

                elif button["name"] == "white_button":
                    Tiles.open_gates.add("White")
                    button["pressed"] = True

    def break_tiles(self):
       

        for tile in Tiles.tiles:

            if self.rect.colliderect(tile["rect"]):
                if tile["property"].get("type") == "Breakable":
                    if self.rect.colliderect(tile["rect"]):
                        Tiles.broken_tiles.add("Breakable")

    def tp_player_to_bullets(self):
        if self.player.tp_enabled:
            for tile in Tiles.tiles:
                if self.rect.colliderect(tile["rect"]):
                    self.player.rect.center = self.rect.center
                    self.player.pos = pygame.Vector2(self.player.rect.center)
            
                    self.player.tp_enabled = False



    

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle -180)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.rect.x += self.velocity.x * Settings.time_multiplyer
        self.rect.y += self.velocity.y * Settings.time_multiplyer

        if not self.ghost:
            for tile in Tiles.tiles:
                if self.rect.colliderect(tile["rect"]):
                    self.kill()
                    break

                    

        if (
        self.rect.right < 0
        or self.rect.left > 1200
        or self.rect.bottom < 0
        or self.rect.top > 800
        ):
            self.kill()

        self.kill_bad_guys()
        self.button_detection_bullets()
        self.break_tiles()
        self.tp_player_to_bullets()
        
###############################################################################################################


def restart_all():
    global map_file, start_x, start_y
    global bullet_max
    global goal_x, goal_y
    global m_stars, m_stars_required
    global kill_is_req, kills_req
    global star, star_rect, star_polygon
    global mini_stars_list
    global m_star_collected
    global bonus_time

    player_group.sprite.reset_player()

    for bullet in bullet_group:
        bullet.kill()

    (
        map_file,
        start_x,
        start_y,
        
        bullet_max,
        goal_x,
        goal_y,
        m_stars,
        m_stars_required,
        kill_is_req,
        kills_req,
        bonus_time
    ) = Settings.level_load()

    Settings.kill_count = 0
    Settings.bullet_count = 0
    Settings.time_multiplyer = 1.0
    Settings.slow_time_active = False
    
    m_star_collected = False
    mini_stars_list = create_mini_stars()
    star, star_rect, star_polygon = create_star(goal_x, goal_y)

    Settings.time = 0

    timer.reset_time()

    Tiles.abilities.clear()
    Tiles.bad_guys.clear()
    Tiles.portals.clear()
    Tiles.buttons.clear()
    Tiles.open_gates.clear()

    for obj in Tiles.bad_guys:
        obj["killed"] = False

    for ability in Tiles.abilities:
        ability["collected"] = False

    for button in Tiles.buttons:
        button["pressed"] = False

    for tile in Tiles.tiles:
        tile["alpha"] = 255
    
    Tiles.load_level(map_file)


player_group = pygame.sprite.GroupSingle()

player = Player(start_x, start_y)
player_group.add(player)

bullet_group = pygame.sprite.Group()
#################################################################################################################
#Game loop ONLY

while True:
    #event loop ONLY
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

                    if hint_button_rect.collidepoint(event.pos):
                        Settings.game_state = "getting_hint"

                    if gun_select_rect.collidepoint(event.pos):
                        Settings.game_state = "gun_select"
            
                case"playing":

                    dialogue_clicked = player_group.sprite.level_start_dialogue()

                    if pause_rect.collidepoint(event.pos):
                        Settings.paused = True
                        timer.pause()


                    if Settings.paused == False and dialogue_clicked != True:
                        
                        barrel = player_group.sprite.barrel_position()
                        if Settings.bullet_count < bullet_max:
                            bullet = Bullet(barrel, player_group.sprite.angle, player_group.sprite)
                            bullet_group.add(bullet)
                            Settings.bullet_count += 1
                            gun_fired_fx.play()

                            player_group.sprite.recoil(bullet.velocity)
                            player_group.sprite.gravity_enabled = True
                            if Settings.playing_state == "start":
                                timer.start()
                                Settings.playing_state = "in_proggress"

                            if player_group.sprite.frozen:
                                player_group.sprite.frozen = False

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
                            #if button.level <= Settings.max_player_level:
                                current_level = button.level
                                Settings.player_level = current_level
                        
                                restart_all()

                                Settings.game_state = "playing"
                                Settings.playing_state = "start"
                                Settings.paused = False
                                player_group.sprite.load_room()

                case "gun_select":
                    for button in gun_selection:

                        if button.rect.collidepoint(event.pos):
                            if Settings.total_stars >= button.gun * 6:
                                Settings.gun = button.gun + 1
                                player_group.sprite.change_gun()
                                Settings.game_state = "start_menu"




                case "lost":
                    if restart_button_rect.collidepoint(event.pos):
                        Settings.playing_state = "start"
                        Settings.game_state = "playing"

                    restart_all()

                    continue

                case "has_won":

                    dialogue_clicked2 = player_group.sprite.level_won_dialogue()

                    if dialogue_clicked2 != True:



                        if next_level_rect.collidepoint(event.pos):
                            Settings.player_level += 1
                            Settings.playing_state = "start"
                            Settings.game_state = "playing"

                            restart_all()
                        
                    continue

                case "getting_hint":
                    for box in check_boxes:
                        if box.rect.collidepoint(event.pos):
                            laugh.play()
                            box.checked = True








#Non-events below
###################################################################################################################

    match Settings.game_state:
        case "start_menu":
            Settings.paused = False
            screen.blit(start_surface, (0,0))
            screen.blit(start_button, start_button_rect)
            screen.blit(s_text, s_text_rect)
            screen.blit(level_button, level_button_rect2)
            screen.blit(hint_button, hint_button_rect)
            screen.blit(gun_select, gun_select_rect)
            
            

            
            if start_music == True:
                #play_music()
                start_music = False

        
        case "playing":



            
            if start_music == False:
                pygame.mixer.music.stop()

            

            screen.blit(bg_surface, (0,0))
            
           
            
        
            Tiles.draw_map(screen)

            screen.blit(pause_surface, pause_rect)


            if Settings.paused == False:

                if player_group.sprite.frozen:
                    player_group.sprite.frozen_update()
                else:
                    player_group.update()
                    player_group.sprite.gravity_enabled = True

                    bullet_group.update()
                    timer.update()

            bullet_group.draw(screen)
            player_group.draw(screen)
            timer.display_timer(screen)
            player_group.sprite.mini_star_load()
            player_group.sprite.level_complete()
            player_group.sprite.load_buttons()
            player_group.sprite.clock_image_load()
            player_group.sprite.rotation_load()
            player_group.sprite.bullet_pickup_load()
            player_group.sprite.slow_time_load()
            player_group.sprite.gravity_swap_load()
            player_group.sprite.load_tp_bullet()
            player_group.sprite.ghost_bullet_load()
            

            for obj in Tiles.bad_guys:
                if not obj["killed"]:
                    screen.blit(bad_guy_surface, obj["rect"])

            if Dialogue.dialogue_active[Settings.player_level - 1][0] == True:  
                dialogue.get_chosen_dialogue()
                dialogue.get_word_list()
                dialogue.display_text_bg()
                dialogue.display_text()
        
            match Settings.playing_state:
                case "start":
                    if not Settings.paused:
                        restart_all()
                        player_group.sprite.follow_mouse()
                        player_group.sprite.retical_line()
                    

                case "in_proggress":
                    if not Settings.paused:
                        player_group.sprite.start_spin()
                        player_group.sprite.gravity_enabled = True

                        r = pygame.key.get_pressed()
                    
                        if r[pygame.K_r]:
                            Settings.time += 1
                            if Settings.time >= 120:
                                Settings.playing_state = "start"
                                restart_all()

                        if Settings.slow_time_active:
                            if pygame.time.get_ticks() - Settings.slow_time_start >= 3000:
                                Settings.time_multiplyer = 1.0
                                Settings.slow_time_active = False
                        

        case "lost":
            screen.blit(loss_screen, loss_screen_rect)
            screen.blit(restart_button, restart_button_rect)


        case "has_won":
            Settings.level_lock()


            

            screen.blit(win_screen, win_screen_rect)
            screen.blit(next_level,next_level_rect)
            timer.display_timer(screen)
            player_group.sprite.normal_star()
            player_group.sprite.bonus_time_star()
            player_group.sprite.bonus_bullet_star()

            if Dialogue.dialogue_active[Settings.player_level - 1][1] == True:  
                dialogue.get_chosen_dialogue()
                dialogue.get_word_list()
                dialogue.display_text_bg()
                dialogue.display_text()

#
        case "selecting_level":
            Settings.paused = False
            screen.blit(level_select_BG, (0,0))
            level_selection.draw(screen)

            lock_level_image(Settings.max_player_level)


        case "getting_hint":
            screen.blit(hint_bg, (0,0))
            screen.blit(Waiver.signature_surface, Waiver.signature_rect)
            check_boxes.draw(screen)
            screen.blit(waiver_text_render, waiver_rect)
            for box in check_boxes:
                if box.checked:
                    screen.blit(checked_box, box.rect)
            

            if pygame.mouse.get_pressed()[0]:
                Waiver.draw_signature(Settings.signing)
                Settings.signing = True
            else:
                Settings.signing = False


        case "gun_select":
            screen.blit(gun_select_bg, (0,0))
            gun_selection.draw(screen)

    
    if Settings.paused:
            
        screen.blit(pause_menu, pause_menu_rect)
        screen.blit(home_surface, home_rect)
        screen.blit(cont_surface, cont_rect)
        screen.blit(level_button, level_button_rect)



    

    
    
    pygame.display.update()
    game_clock.tick(60)
    
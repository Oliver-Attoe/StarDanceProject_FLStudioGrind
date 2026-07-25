import pygame
from sys import exit
import math
import pytmx
from pytmx.util_pygame import load_pygame


pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

GRAVITY = 2
game_state = "start_menu"
playing_state = "start"

start_screen_sound = pygame.mixer.music.load("Sounds/human_music.mp3")
pygame.mixer.music.play(-1)
button_fx = pygame.mixer.Sound("Sounds/button_pressed.mp3")
gun_fired_fx = pygame.mixer.Sound("Sounds/bullet_fired.mp3")

tmx_data = load_pygame("Maps/place_holder_map.tmx")
collision_rects = []


def draw_map(surface, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    surface.blit(
                        tile,
                        (x * tmx_data.tilewidth,
                         y * tmx_data.tileheight)
                    )


start_surface = pygame.image.load("Images/Start screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (600, 125))
start_button  = pygame.image.load("Images/Button.png").convert()
start_button_rect = start_button.get_rect(center = (600,400))

#This section is sisplayed in playing game state
bg_surface = pygame.image.load("Images/BG.png").convert()
floor_surface = pygame.image.load("Images/Floor.png").convert()
floor_rect = floor_surface.get_rect(midbottom = (600, 800))

x = 500
y = 575


                    


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(600, 550))
        self.mask = pygame.mask.from_surface(self.image)

        self.gravity_enabled = False

        self.angle = 0

        self.barrel_offset = pygame.Vector2(30,12)
        
        self.p_velocity = pygame.Vector2(0, 0)

       

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
           
    def barrel_position(self):
        rotated_offset = self.barrel_offset.rotate(-(self.angle))
        return pygame.Vector2(self.rect.center) + rotated_offset
    
    def recoil(self,velocity):
        self.p_velocity -= velocity

    def in_air_rotate(self):
        self.angle += 4

    #def collision(self):


    def update(self):
        if self.gravity_enabled == True:
            self.rect.y += GRAVITY

        self.image = pygame.transform.rotate(self.original_image, self.angle -180)
        
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)


        self.p_velocity *= 0.975
        self.rect.x += self.p_velocity.x
        self.rect.y += self.p_velocity.y




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

obstacle_group = pygame.sprite.Group()


#Game loop
while True:
    #event loop only
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos) and game_state == "start_menu":
                button_fx.play()
                game_state = "playing"
                

            elif game_state == "playing":
                gun_fired_fx.play()
                playing_state = "in_proggress"
                player_group.sprite.gravity_enabled = True
                barrel = player_group.sprite.barrel_position()

                bullet = Bullet(barrel, player_group.sprite.angle)
                bullet_group.add(bullet)

                player_group.sprite.recoil(bullet.velocity)


    if game_state == "start_menu":
        screen.blit(start_surface, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(s_text, s_text_rect)
        


    elif game_state == "playing":
        pygame.mixer.music.stop()
        screen.blit(bg_surface, (0,0))
        screen.blit(floor_surface,floor_rect)
        draw_map(screen, tmx_data)
        

        if playing_state == "start":
            player_group.sprite.follow_mouse()
            player_group.sprite.retical_line()
            

        if playing_state == "in_proggress":
            player_group.sprite.in_air_rotate()

        player_group.update()

        bullet_group.update()
        bullet_group.draw(screen)


      
        player_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
    
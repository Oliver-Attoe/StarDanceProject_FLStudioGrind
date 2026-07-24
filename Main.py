import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

GRAVITY = 2
game_state = "start_menu"
playing_state = "start"

start_surface = pygame.image.load("Images/Start screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (500, 125))
start_button  = pygame.image.load("Images/Button.png").convert()
start_button_rect = start_button.get_rect(center = (500,400))

#This section is sisplayed in playing game state
bg_surface = pygame.image.load("Images/Background_1.png").convert()
floor_surface = pygame.image.load("Images/Floor.png").convert()
floor_rect = floor_surface.get_rect(midbottom = (500, 800))

x = 500
y = 575

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 550))

        self.barrel_offset = pygame.Vector2(25,12)
        self.p_velocity = pygame.Vector2(0, 0)
        
        self.gravity_active = False
       

    def follow_mouse(self,x ,y):
        #image rotation follows mouse movement
        self.m_pos = pygame.mouse.get_pos()

        x_dist = self.m_pos[0] - self.rect.centerx
        y_dist = -(self.m_pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        old_center = self.rect.center

        self.image = pygame.transform.rotate(self.original_image, self.angle - 180)
        self.rect = self.image.get_rect(center=old_center)

        self.barrel_pos = self.barrel_offset.rotate(-self.angle) + self.rect.center

    def retical_line(self):
        #line starts at barrel, ends at mouse location
        pygame.draw.line(screen, "white", self.barrel_pos, pygame.mouse.get_pos(), 3)


    def recoil(self,velocity):
        self.p_velocity -= velocity

    def update(self):
        if self.gravity_active == True:
            self.rect.y += GRAVITY

        self.p_velocity *= 0.97
        self.rect.x += self.p_velocity.x
        self.rect.y += self.p_velocity.y




class Bullet(pygame.sprite.Sprite):
    def __init__(self, barrel_pos, m_pos):
        super().__init__()

        self.image = pygame.image.load("Images/BULLET.png").convert_alpha()
        self.rect = self.image.get_rect(center=barrel_pos)

        direction = pygame.Vector2(
            m_pos[0] - barrel_pos[0],
            m_pos[1] - barrel_pos[1]
        )

        if direction.length() > 0:
            direction = direction.normalize()

        self.velocity = direction * 10



    

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.centerx <= 0 or self.rect.centerx >= 1000:
            self.kill()

        if self.rect.centery <=0 or self.rect.centery >=800:
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
            if start_button_rect.collidepoint(event.pos):
                game_state = "playing"
            
            elif game_state == "playing":
                player_group.sprite.gravity_active = True
                playing_state = "in_progress"

                bullet = Bullet(player_group.sprite.barrel_pos, player_group.sprite.m_pos)
                bullet_group.add(bullet)

                player_group.sprite.recoil(bullet.velocity)


    if game_state == "start_menu":
        screen.blit(start_surface, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(s_text, s_text_rect)

    elif game_state == "playing":
        if player_group.sprite.gravity_active == True:
            player_group.sprite.update()

        screen.blit(bg_surface, (0,0))
        screen.blit(floor_surface,floor_rect)

        bullet_group.update()
        bullet_group.draw(screen)

        
        player_group.update()
        player_group.sprite.follow_mouse(x, y)      
        player_group.draw(screen)

        if playing_state == "start":
            player_group.sprite.retical_line()




    pygame.display.update()
    clock.tick(60)
    
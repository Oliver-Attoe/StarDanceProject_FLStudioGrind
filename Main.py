import pygame
from sys import exit
import math

x = 500
y = 575

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("Images/GUN.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 550))
        self.barrel_offset = pygame.Vector2(25,12)

        self.gravity_active = False
        self.gravity = 0        

    def follow_mouse(self,x ,y):
        #image rotation follows mouse movement
        m_pos = pygame.mouse.get_pos()

        x_dist = m_pos[0] - self.rect.centerx
        y_dist = -(m_pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        old_center = self.rect.center

        self.image = pygame.transform.rotate(self.original_image, self.angle - 180)
        self.rect = self.image.get_rect(center=old_center)


    def retical_line(self):
        #line starts at barrel, ends at mouse location
        barrel_pos = self.barrel_offset.rotate(-self.angle)
        barrel_pos += self.rect.center

        pygame.draw.line(screen, "white", barrel_pos, pygame.mouse.get_pos(), 3)

    def gravity_apply(self):
        self.gravity = 2
        self.rect.y += self.gravity



pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player(x, y))

#This section is displayed in start game state
game_state = "start_menu"
start_surface = pygame.image.load("Images/Start screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (500, 125))
start_button  = pygame.image.load("Images/Button.png").convert()
start_button_rect = start_button.get_rect(center = (500,400))

#This section is sisplayed in playing game state
## p = player, bg = background
bg_surface = pygame.image.load("Images/Background_1.png").convert()
floor_surface = pygame.image.load("Images/Floor.png").convert()
floor_rect = floor_surface.get_rect(midbottom = (500, 800))

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
                player.sprite.gravity_active = True

    if game_state == "start_menu":
        screen.blit(start_surface, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(s_text, s_text_rect)

    elif game_state == "playing":
        if player.sprite.gravity_active == True:
            player.sprite.gravity_apply()


        screen.blit(bg_surface, (0,0))
        screen.blit(floor_surface,floor_rect)
        player.sprite.follow_mouse(x, y)
        player.draw(screen)
        player.sprite.retical_line()


    pygame.display.update()
    clock.tick(60)
    
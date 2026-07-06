import pygame
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

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
p_surface = pygame.image.load("Images/Gun_final.png").convert_alpha() #Chnage to alpha later
x = 500
y = 575

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


    if game_state == "start_menu":
        screen.blit(start_surface, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(s_text, s_text_rect)

    elif game_state == "playing":
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - x
        y_dist = -(pos[1] - y)
        angle = math.degrees(math.atan2(y_dist, x_dist))

        p_rotate = pygame.transform.rotate(p_surface, angle - 90)
        p_rect = p_rotate.get_rect(center = (x, y))

        screen.blit(bg_surface, (0,0))
        screen.blit(floor_surface, (0, 725))
        screen.blit(p_rotate, p_rect)
        
        if p_rect.bottom >= 725: p_rect.bottom = 725

        



    pygame.display.update()
    clock.tick(60)
    
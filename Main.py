import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

#This section is all to do with start screen
game_state = "start_menu"
start_surface = pygame.image.load("Images/Start screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (500, 125))
start_button  = pygame.image.load("Images/Button.png").convert()
start_button_rect = start_button.get_rect(center = (500,400))

#This section is to do with main game
bg_surface = pygame.image.load("Images/Background_1.png").convert()

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == "start_menu":
            screen.blit(start_surface, (0,0))
            screen.blit(start_button, start_button_rect)
            screen.blit(s_text, s_text_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_state = "playing"
                    
        elif game_state == "playing":
            screen.blit(bg_surface, (0,0))
           

    pygame.display.update()
    clock.tick(60)
    
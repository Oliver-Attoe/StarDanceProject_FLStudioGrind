import pygame
pygame.init()

screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

#Images
BG_surface = pygame.image.load("Images/Background_1.png").convert()
floor_surface = pygame.image.load("Images/Floor.png").convert()
floor_rect = floor_surface.get_rect(midbottom = (500, 800))

player = pygame.image.load("Images/Player_Placeholder.png").convert_alpha()
player_rect = player.get_rect(midbottom = (500,0))

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player_rect.y -= 50
    screen.blit(BG_surface, (0,0))
    screen.blit(floor_surface, floor_rect)
    screen.blit(player, player_rect)

    #Gravity (needs work but basic)
    if player_rect.colliderect(floor_rect) == 0:
        player_rect.y += 2.225
    
    pygame.display.update()
    clock.tick(60)
    
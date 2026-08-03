import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
from Settings import levels



start_surface = pygame.image.load("Images/Start_screen.png").convert()
s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")

number_text_load = pygame.font.Font("Images/DigitalDreamers-jy99.ttf", 30)

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

level_button = pygame.image.load("Images/Level_button_pause.png")
level_button_rect = level_button.get_rect(center = (500, 400))
level_button_rect2 = level_button.get_rect(topleft = (10, 745) )

level_select_BG = pygame.image.load("Images/Level_select_BG.png")

loss_screen = pygame.image.load("Images/Loss_screen.png")
loss_screen_rect = loss_screen.get_rect(center = (600, 400))

restart_button = pygame.image.load("Images/Restart_button.png")
restart_button_rect = restart_button.get_rect(center = (600, 400))


class Level_select(pygame.sprite.Sprite):
    def __init__(self, level, x, y):
        super().__init__()

        self.image = pygame.image.load("Images/Level_button.png")
        self.rect = self.image.get_rect(center = (x,y))
        self.level = level
        level_button_numb = number_text_load.render (str(level), True, "Black")

        text_rect = level_button_numb.get_rect(center=self.image.get_rect().center)

        self.image.blit(level_button_numb, text_rect)
        

level_group = pygame.sprite.Group()
        
def button_generation(levels):            
        

        x = 360
        y = 260

        for level in range(1, levels + 1):
            level_button = Level_select(level, x, y)
            level_group.add(level_button)
            x += 120
            if x >= 960:
                x = 360
                y += 120

        return level_group









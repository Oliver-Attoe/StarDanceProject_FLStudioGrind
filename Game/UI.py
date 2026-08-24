import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
from Settings import levels, max_player_level, gun, total_stars









start_surface = pygame.image.load("Images/Start_screen.png").convert()

s_text_test = pygame.font.Font("Images/SpyAgencyBoldItalic-BLLnV.otf", 60)
s_text = s_text_test.render ("Barrel Roll Bullet", True, "Black")
s_text_rect = s_text.get_rect(center = (600, 125))

number_text_load = pygame.font.Font("Images/DigitalDreamers-jy99.ttf", 30)


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
level_button_rect2 = level_button.get_rect(bottomleft = (10, 790) )

level_select_BG = pygame.image.load("Images/Level_select_BG.png")

loss_screen = pygame.image.load("Images/Loss_screen.png")
loss_screen_rect = loss_screen.get_rect(center = (600, 400))

restart_button = pygame.image.load("Images/Restart_button.png")
restart_button_rect = restart_button.get_rect(center = (600, 400))

win_screen = pygame.image.load("Images/Win_screen.png")
win_screen_rect = win_screen.get_rect(center = (600,400))

next_level = pygame.image.load("Images/Next_level.png")
next_level_rect = next_level.get_rect(center = (600,400))

timer_text = pygame.font.Font("Images/timer_text.ttf", 90)

mini_star = pygame.image.load("Images/Mini_star.png").convert_alpha()

clock_surafce = pygame.image.load("Images/clock.png").convert_alpha()

bad_guy_surface = pygame.image.load("Images/3 bad guys.png")

purple_button = pygame.image.load("Images/purple_button.png").convert_alpha()
green_button = pygame.image.load("Images/green_button.png").convert_alpha()
white_button = pygame.image.load("Images/white_button.png").convert_alpha()

locked_surface = pygame.image.load("Images/Locked.png").convert_alpha()

signature_square = pygame.image.load("Images/signature_square.png")


hint_button = pygame.image.load("Images/hint_button.png")
hint_button_rect = hint_button.get_rect(bottomright = (1190, 790))

hint_bg = pygame.image.load("Images/hint_BG.png")

unchecked_box = pygame.image.load("Images/unchecked_box.png")
checked_box = pygame.image.load("Images/checked_box.png")

waiver_text =  pygame.font.Font("Images/Times_new.ttf", 90)
waiver_text_render = waiver_text.render ("Terms and Conditions", True, "Black")
waiver_rect = waiver_text_render.get_rect(center = (600, 65))

rotation_arrow = pygame.image.load("Images/rotation_arrow.png")

bullet_pickup_surface = pygame.image.load("Images/bullet_pickup.png")

slow_time_surface = pygame.image.load("Images/Slow_time.png")

gravity_swap_surface = pygame.image.load("Images/Gravity_swap.png")

tp_bullet = pygame.image.load("Images/tp_bullet.png")

ghost_bullet = pygame.image.load("Images/ghost_bullet.png")

gun_select = pygame.image.load("Images/gun_select.png")
gun_select_rect = gun_select.get_rect(midbottom = (600, 800))
gun_select_bg = pygame.image.load("Images/gun_select_BG.png")

go_back = pygame.image.load("Images/Go_back.png")
go_back_rect = go_back.get_rect(topright = (1200, 0))

waiver_text_box = pygame.Rect(900, 200, 250, 500)

get_hint_surface = pygame.image.load("Images/Get_hint.png")
get_hint_rect = get_hint_surface.get_rect(bottomright = (1180, 780))

class Level_select(pygame.sprite.Sprite):
    def __init__(self, level, x, y):
        super().__init__()

        self.image = pygame.image.load("Images/Level_button.png")
        self.rect = self.image.get_rect(center = (x,y))
        self.level = level
        level_button_numb = number_text_load.render (str(level), True, "Black")

        text_rect = level_button_numb.get_rect(center=self.image.get_rect().center)

        self.image.blit(level_button_numb, text_rect)

class Gun_select(pygame.sprite.Sprite):
    def __init__(self,gun, x, y):
        super().__init__()
###############################CHANGE BUTTONS LATER PLEASE, AND THE NUMBERS DISPLAYED ONTO #############################
        self.image = pygame.image.load("Images/Level_button.png")
        self.rect = self.image.get_rect(center = (x,y))
        self.gun = gun


        

level_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
        
def button_generation(levels):            
        

        x = 360
        y = 330

        for level in range(1, levels + 1):
            level_button = Level_select(level, x, y)
            level_group.add(level_button)
            x += 120
            if x >= 960:
                x = 360
                y += 120

            

        return level_group

def lock_level_image(max_player_level):
    for level_button in level_group:
        if level_button.level > max_player_level:
            screen.blit(locked_surface, level_button.rect)
            



def create_star(goal_x, goal_y):
    star = pygame.image.load("Images/star2.png").convert_alpha()
    star_rect = star.get_rect(center=(goal_x, goal_y))

    local_star_polygon = [
        pygame.Vector2(0, -55),  # 1
        pygame.Vector2(55, -10),   # 2
        pygame.Vector2(35, 55),    # 4
        pygame.Vector2(-35, 55),    # 5
        pygame.Vector2(-55, -10),
    ]

    star_polygon = []
    centre = pygame.Vector2(star_rect.center)

    for point in local_star_polygon:
        star_polygon.append(centre + point)



    return star, star_rect,star_polygon

def create_mini_stars():

    mini_star_rect = mini_star.get_rect(center=(150, 200))

    mini_star_rect2 = mini_star.get_rect(center=(150, 470))
    
     
    local_m_star_polygon = [
            pygame.Vector2(0, -45),  # 1
             pygame.Vector2(0, 45),   # 2
             pygame.Vector2(45, 0),    # 4
             pygame.Vector2(-45, 0),    # 5
         ]
     
    mini_star_polygon = []
    centre = pygame.Vector2(mini_star_rect.center)
     
    for point in local_m_star_polygon:
        mini_star_polygon.append(centre + point)

    mini_star_polygon2 = []
    centre2 = pygame.Vector2(mini_star_rect2.center)
     
    for point in local_m_star_polygon:
        mini_star_polygon2.append(centre2 + point)


    mini_stars_list = [
        {
        "rect": mini_star_rect,
        "polygon": mini_star_polygon,
        "collected": False
        },
        {
        "rect": mini_star_rect2,
        "polygon": mini_star_polygon2,
        "collected": False
        }
    ]
        
     
     
    return mini_stars_list



def gun_button_generation():            
        

        x = 360
        y = 330

        for gun_number in range(10):
            gun_button = Gun_select(gun_number, x, y)
            gun_group.add(gun_button)
            x += 120
            if x >= 960:
                x = 360
                y += 120

            

        return gun_group

def lock_gun_image(total_stars):
    for button in gun_group:
        if total_stars < button.gun * 6:
           screen.blit(locked_surface, button.rect)






import pygame
from UI import checked_box, screen, waiver_text_box

last_position = None
signature_surface = pygame.Surface((500, 250), pygame.SRCALPHA)
signature_rect = signature_surface.get_rect(topleft=(50, 500))

text_active = True
letters = []
new_waiver_text = pygame.font.Font("Images/Times_new.ttf", 30)

def draw_signature(signing):
    global last_position
    global signature_surface
    

    mouse_position = pygame.mouse.get_pos()

    local_position = (
        mouse_position[0] - signature_rect.x,
        mouse_position[1] - signature_rect.y
    )


    if signing == False:
        local_position = None
        last_position =  None

    if last_position is not None:
        pygame.draw.line(
            signature_surface,
            (225, 0, 0),
            last_position,
            local_position,
            5
        )


    last_position = local_position

class Check_boxes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("Images/unchecked_box.png")
        self.rect = self.image.get_rect(center = (x,y))
        self.checked = False



        

check_box_group = pygame.sprite.Group()
        
def check_box_generation(screen, unchecked_box):            
        

        x = 80
        y = 400

        for box in range(1, 4):
            check_box = Check_boxes(x, y)
            check_box_group.add(check_box)
            screen.blit(unchecked_box, (x,y))
            y -= 100


        return check_box_group 

class Text_box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()



        
def text_box():
    x = waiver_text_box.midleft[0] + 10
    y = waiver_text_box.midtop[1] + 10
    if text_active:
        for letter in letters:
            font_render = new_waiver_text.render(letter, True, "Black")
            screen.blit(font_render, (x,y))
            x += 18

            if x >= waiver_text_box.midright[0] - 10:
                y += 35
                x = waiver_text_box.midleft[0] + 10


     






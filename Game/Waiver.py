import pygame
from UI import checked_box, screen, waiver_text_box

last_position = None
signature_surface = pygame.Surface((500, 250), pygame.SRCALPHA)
signature_rect = signature_surface.get_rect(topleft=(50, 500))
sig_field_filled = False
text_field_filled = False

text_active = True
text_visible = True
text = ""
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






        
def text_box():
    if not text_visible:
        return

    x = waiver_text_box.left + 10
    y = waiver_text_box.top + 10

    lines = text.split("\n")

    for line in lines:
        words = line.split(" ")

        for word in words:
            font_render = new_waiver_text.render(word, True, "Black")
            word_width = font_render.get_width()

            if x + word_width > waiver_text_box.right - 10:
                x = waiver_text_box.left + 10
                y += 35

            if y + font_render.get_height() <= waiver_text_box.bottom - 10:
                screen.blit(font_render, (x, y))

            x += word_width
            x += new_waiver_text.size(" ")[0]

        x = waiver_text_box.left + 10
        y += 35

def all_fields_filled():
    field_count = 0

    for box in check_box_group:
        if box.checked:
            field_count += 1

    if sig_field_filled:
        field_count += 1

    if text_field_filled:
        field_count += 1

    return field_count



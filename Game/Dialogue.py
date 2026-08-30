import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
import Settings

dialogue_active = [[True, True] for _ in range(Settings.levels)]


class Dialogue(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Game/Images/Dialogue_box.png")
        self.rect = self.image.get_rect(center=(600, 675))

        self.text = ""
        self.word_list = []

        self.font = pygame.font.Font(
            "Game/Images/undertale_font.ttf",
            50
        )

        self.text_delay = 210
        self.last_word_time = pygame.time.get_ticks()

        self.word_index = 0

        self.x = self.rect.topleft[0] + 40
        self.y = self.rect.topleft[1] + 25

        self.active = True
        

    def get_chosen_dialogue(self, dialogue_type):

        

        match Settings.player_level:

            case 1:
                if dialogue_type == "start":
                    return "Level 1 start dialogue"
                elif dialogue_type == "won":
                    return "Level 1 win dialogue"

            case 2:
                if dialogue_type == "start":
                    return "Level 2 start dialogue"
                elif dialogue_type == "won":
                    return "Level 2 win dialogue"

        return ""

    def start_dialogue(self, dialogue_type):

        self.text = self.get_chosen_dialogue(dialogue_type)

        self.get_word_list()

        self.word_index = 0
        self.last_word_time = pygame.time.get_ticks()

        self.active = True
        
    def get_word_list(self):
        self.word_list = self.text.split(" ")

    def display_text_bg(self):

        if not self.active:
            return

        screen.blit(self.image, self.rect)

    def display_text(self):

        if not self.active:
            return

        current_time = pygame.time.get_ticks()

        if self.word_index < len(self.word_list):

            if current_time - self.last_word_time >= self.text_delay:
                self.word_index += 1
                self.last_word_time = current_time



        x = self.rect.topleft[0] + 40
        y = self.rect.topleft[1] + 15

        for word in self.word_list[:self.word_index]:

            font_render = self.font.render(word, True, "White")
            word_width = font_render.get_width()
            

            if x + word_width >= 1000:
                y += 60
                x = self.rect.topleft[0] + 40

            screen.blit(font_render, (x, y))

            x += word_width + 20




        
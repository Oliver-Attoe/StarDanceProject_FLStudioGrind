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
            case 0:
                if dialogue_type == "start":
                    return "Strange, there is a man here..."
                elif dialogue_type == "won":
                    return "You recieve an egg... and a new gun skin (;)"

            case 1:
                if dialogue_type == "start":
                    return "Use mouse to aim your first shot, fire with enter or left mouse button. ALSO. Hold r to restart"
                elif dialogue_type == "won":
                    return "WOW! Looks like somebody's getting the hang of things"

            case 2:
                if dialogue_type == "start":
                    return "If you get stuck, you can hold a to re-align yourself"
                elif dialogue_type == "won":
                    return "Each level has a bullet count and time completed bonus objective, giving you a star.."

            case 3:
                if dialogue_type == "start":
                    return "You can use stars to get cool new gun skins"
                elif dialogue_type == "won":
                    return "This is too easy, lets try something new"

            case 4:
                if dialogue_type == "start":
                    return "I'm sure you can guess what will happen if you colide with those _______"
                elif dialogue_type == "won":
                    return "Good Job!"

            case 5:
                if dialogue_type == "start":
                    return ""
                elif dialogue_type == "won":
                    return "Level 5 win dialogue"

            case 6:
                if dialogue_type == "start":
                    return "Level 6 start dialogue"
                elif dialogue_type == "won":
                    return "Level 6 win dialogue"

            case 7:
                if dialogue_type == "start":
                    return "Level 7 start dialogue"
                elif dialogue_type == "won":
                    return "Level 7 win dialogue"

            case 8:
                if dialogue_type == "start":
                    return "Level 8 start dialogue"
                elif dialogue_type == "won":
                    return "Level 8 win dialogue"

            case 9:
                if dialogue_type == "start":
                    return "Level 9 start dialogue"
                elif dialogue_type == "won":
                    return "Level 9 win dialogue"

            case 10:
                if dialogue_type == "start":
                    return "Level 10 start dialogue"
                elif dialogue_type == "won":
                    return "Level 10 win dialogue"

            case 11:
                if dialogue_type == "start":
                    return "Level 11 start dialogue"
                elif dialogue_type == "won":
                    return "Level 11 win dialogue"

            case 12:
                if dialogue_type == "start":
                    return "Level 12 start dialogue"
                elif dialogue_type == "won":
                    return "Level 12 win dialogue"

            case 13:
                if dialogue_type == "start":
                    return "Level 13 start dialogue"
                elif dialogue_type == "won":
                    return "Level 13 win dialogue"

            case 14:
                if dialogue_type == "start":
                    return "Level 14 start dialogue"
                elif dialogue_type == "won":
                    return "Level 14 win dialogue"

            case 15:
                if dialogue_type == "start":
                    return "Level 15 start dialogue"
                elif dialogue_type == "won":
                    return "Level 15 win dialogue"

            case 16:
                if dialogue_type == "start":
                    return "Level 16 start dialogue"
                elif dialogue_type == "won":
                    return "Level 16 win dialogue"

            case 17:
                if dialogue_type == "start":
                    return "Level 17 start dialogue"
                elif dialogue_type == "won":
                    return "Level 17 win dialogue"

            case 18:
                if dialogue_type == "start":
                    return "Level 18 start dialogue"
                elif dialogue_type == "won":
                    return "Level 18 win dialogue"

            case 19:
                if dialogue_type == "start":
                    return "Level 19 start dialogue"
                elif dialogue_type == "won":
                    return "Level 19 win dialogue"

            case 20:
                if dialogue_type == "start":
                    return "Level 20 start dialogue"
                elif dialogue_type == "won":
                    return "Level 20 win dialogue"

            case 21:
                if dialogue_type == "start":
                    return "Level 21 start dialogue"
                elif dialogue_type == "won":
                    return "Level 21 win dialogue"

            case 22:
                if dialogue_type == "start":
                    return "Level 22 start dialogue"
                elif dialogue_type == "won":
                    return "Level 22 win dialogue"

            case 23:
                if dialogue_type == "start":
                    return "Level 23 start dialogue"
                elif dialogue_type == "won":
                    return "Level 23 win dialogue"

            case 24:
                if dialogue_type == "start":
                    return "Level 24 start dialogue"
                elif dialogue_type == "won":
                    return "Level 24 win dialogue"

            case 25:
                if dialogue_type == "start":
                    return "Level 25 start dialogue"
                elif dialogue_type == "won":
                    return "Level 25 win dialogue"

            case 26:
                if dialogue_type == "start":
                    return "Level 26 start dialogue"
                elif dialogue_type == "won":
                    return "Level 26 win dialogue"

            case 27:
                if dialogue_type == "start":
                    return "Level 27 start dialogue"
                elif dialogue_type == "won":
                    return "Level 27 win dialogue"

            case 28:
                if dialogue_type == "start":
                    return "Level 28 start dialogue"
                elif dialogue_type == "won":
                    return "Level 28 win dialogue"

            case 29:
                if dialogue_type == "start":
                    return "Level 29 start dialogue"
                elif dialogue_type == "won":
                    return "Level 29 win dialogue"

            case 30:
                if dialogue_type == "start":
                    return "Level 30 start dialogue"
                elif dialogue_type == "won":
                    return "Level 30 win dialogue"

            case 31:
                if dialogue_type == "start":
                    return "Level 31 start dialogue"
                elif dialogue_type == "won":
                    return "Level 31 win dialogue"

            case 32:
                if dialogue_type == "start":
                    return "Level 32 start dialogue"
                elif dialogue_type == "won":
                    return "Level 32 win dialogue"

            case 33:
                if dialogue_type == "start":
                    return "Level 33 start dialogue"
                elif dialogue_type == "won":
                    return "Level 33 win dialogue"

            case 34:
                if dialogue_type == "start":
                    return "Level 34 start dialogue"
                elif dialogue_type == "won":
                    return "Level 34 win dialogue"

            case 35:
                if dialogue_type == "start":
                    return "Level 35 start dialogue"
                elif dialogue_type == "won":
                    return "Level 35 win dialogue"

            case 36:
                if dialogue_type == "start":
                    return "Level 36 start dialogue"
                elif dialogue_type == "won":
                    return "Level 36 win dialogue"

            case 37:
                if dialogue_type == "start":
                    return "Level 37 start dialogue"
                elif dialogue_type == "won":
                    return "Level 37 win dialogue"

            case 38:
                if dialogue_type == "start":
                    return "Level 38 start dialogue"
                elif dialogue_type == "won":
                    return "Level 38 win dialogue"

            case 39:
                if dialogue_type == "start":
                    return "Level 39 start dialogue"
                elif dialogue_type == "won":
                    return "Level 39 win dialogue"

            case 40:
                if dialogue_type == "start":
                    return "Level 40 start dialogue"
                elif dialogue_type == "won":
                    return "Level 40 win dialogue"

            case 41:
                if dialogue_type == "start":
                    return "Level 41 start dialogue"
                elif dialogue_type == "won":
                    return "Level 41 win dialogue"

            case 42:
                if dialogue_type == "start":
                    return "Level 42 start dialogue"
                elif dialogue_type == "won":
                    return "Level 42 win dialogue"

            case 43:
                if dialogue_type == "start":
                    return "Level 43 start dialogue"
                elif dialogue_type == "won":
                    return "Level 43 win dialogue"

            case 44:
                if dialogue_type == "start":
                    return "Level 44 start dialogue"
                elif dialogue_type == "won":
                    return "Level 44 win dialogue"

            case 45:
                if dialogue_type == "start":
                    return "Level 45 start dialogue"
                elif dialogue_type == "won":
                    return "Level 45 win dialogue"

            case 46:
                if dialogue_type == "start":
                    return "Level 46 start dialogue"
                elif dialogue_type == "won":
                    return "Level 46 win dialogue"

            case 47:
                if dialogue_type == "start":
                    return "Level 47 start dialogue"
                elif dialogue_type == "won":
                    return "Level 47 win dialogue"

            case 48:
                if dialogue_type == "start":
                    return "Level 48 start dialogue"
                elif dialogue_type == "won":
                    return "Level 48 win dialogue"

            case 49:
                if dialogue_type == "start":
                    return "Level 49 start dialogue"
                elif dialogue_type == "won":
                    return "Level 49 win dialogue"

            case 50:
                if dialogue_type == "start":
                    return "Level 50 start dialogue"
                elif dialogue_type == "won":
                    return "Level 50 win dialogue"

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




        
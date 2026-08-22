import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
from SOUNDS import new_voice_blip
from Settings import levels
import random

dialogue_option = 1
dialogue_active = [[True,True] for _ in range(levels)]



class Dialogue(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/Dialogue_box.png")
        self.rect = self.image.get_rect(center=(600, 675))

        self.text = ""
        self.word_list = []

        self.font = pygame.font.Font(
            "Images/undertale_font.ttf",
            50
        )

        self.text_delay = 210
        self.last_word_time = pygame.time.get_ticks()

        self.word_index = 0
        self.visible_words = []

        self.x = self.rect.topleft[0] + 40
        self.y = self.rect.topleft[1] + 25

    def get_chosen_dialogue(self):
        match dialogue_option:
            case 1:
                self.text = "This is a text, I hope this is working and i hate evil cats and dogs becuase iDK is this text wrapping I hope so"


    def get_word_list(self):
        self.word_list = self.text.split(" ")
        

    def display_text_bg(self):
        if self.word_index > 0:
            if self.x == self.rect.topleft[0] + 40 and self.y == self.rect.topleft[1] + 25:
                screen.blit(self.image, self.rect)


    def display_text(self):
        current_time = pygame.time.get_ticks()

        if self.word_index < len(self.word_list):
            if current_time - self.last_word_time >= self.text_delay:
                self.word_index += 1
                self.last_word_time = current_time
        else:
            new_voice_blip.stop()

        x = self.rect.topleft[0] + 40
        y = self.rect.topleft[1] + 15

        for word in self.word_list[:self.word_index]:
            font_render = self.font.render(word, True, "White")
            word_width = font_render.get_width()

            if x + word_width >= 1000:
                y += 60
                x = self.rect.topleft[0] + 40

            if y >= 770:
                x = self.rect.topleft[0] + 40
                y = self.rect.topleft[1] + 25
                screen.blit(self.image, self.rect)


            screen.blit(font_render, (x, y))
            new_voice_blip.play()
            new_voice_blip.set_volume(0.1)

            x += word_width + 20
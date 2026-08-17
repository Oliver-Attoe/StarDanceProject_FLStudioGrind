import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
from SOUNDS import voice_blip
import random

dialogue_option = 1


class Dialogue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Dialogue_box.png")
        self.rect = self.image.get_rect(center = (600, 675))
        self.text = "not working as intended"

        self.letter_list = []

        self.font = pygame.font.Font("Images/undertale_font.ttf", 50)

        self.text_delay = 150

        self.last_letter_time = pygame.time.get_ticks()

        self.letter_index = 0

    def chosen_dialogue(self):
        match dialogue_option:
            case 1:
                self.text = "Wow it is working, call me Toby fox the way I make these text boxes, this took too long, little side quest, it should be a new screen now i hope???? "

    def get_word_list(self):
        self.letter_list = self.text.split(" ")


    def display_text(self, screen):
        x = self.rect.topleft[0] + 40
        y = self.rect.topleft[1] + 25

        current_time = pygame.time.get_ticks()

        screen.blit(self.image, self.rect)

        if (
            self.letter_index < len(self.letter_list)
            and current_time - self.last_letter_time >= self.text_delay
        ):
            self.letter_index += 1
            self.last_letter_time = current_time

        current_x = x
        current_y = y

        for word in self.letter_list[:self.letter_index]:

            word_surface = self.font.render(
                word + " ",
                True,
                (255, 255, 255)
            )

            word_width = word_surface.get_width()

            if current_x + word_width > self.rect.right - 40:
                current_y += 70
                current_x = x

            screen.blit(
                word_surface,
                (current_x, current_y)
            )
            voice_blip.play()

            current_x += word_width

            if current_y >= 700:
                screen.blit(
                self.image,
                self.rect
            )
                current_x = self.rect.topleft[0] + 40
                current_y  = self.rect.topleft[1] + 25

            if self.letter_index >= len(self.letter_list):
                voice_blip.stop()




                


dialogue_group = pygame.sprite.Group()


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

        self.font = pygame.font.Font("Images/undertale_font.ttf", 30)

        self.text_delay = random.uniform(40, 60)

        self.last_letter_time = pygame.time.get_ticks()

        self.letter_index = 0

    def chosen_dialogue(self):
        match dialogue_option:
            case 1:
                self.text = "Wow it is working, call me Toby fox the way I make these text boxes, this took too long, little side quest, it should be a new screen now i hope???? "

    def get_letter_list(self):
        for char in self.text:
            self.letter_list.append(char)

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

        for letter in self.letter_list[:self.letter_index]:

            text_surface = self.font.render(
                letter,
                True,
                (255, 255, 255)
            )

            screen.blit(
                text_surface,
                (current_x, current_y)
            )

            number = random.uniform(0.7, 1.0)
            voice_blip.set_volume(number)
            voice_blip.play()

            current_x += 20
            if current_x >= 950:
                current_y += 40
                current_x = self.rect.topleft[0] + 40

            if current_y >= 720:
                screen.blit(self.image, self.rect)
                current_x = self.rect.topleft[0] + 40
                current_y = self.rect.topleft[1] + 25



                


dialogue_group = pygame.sprite.Group()


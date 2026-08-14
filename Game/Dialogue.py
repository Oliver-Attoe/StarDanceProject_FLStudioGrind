import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))

dialogue_option = 1


class Dialogue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Dialogue_box.png")
        self.rect = self.image.get_rect(center = (600, 675))
        self.text = "not working as intended"

        self.letter_list = []

        self.font = pygame.font.Font("Images/Times_new.ttf", 30)

        self.text_delay = 50

        self.last_letter_time = pygame.time.get_ticks()

        self.letter_index = 0

    def chosen_dialogue(self):
        match dialogue_option:
            case 1:
                self.text = "bin, there is a bin here, how cool"

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

            current_x += 20
            if current_x >= 600:
                current_y += 75
                current_x = self.rect.topleft[0] + 40


                


dialogue_group = pygame.sprite.Group()

#print (dialogue.letter_list)
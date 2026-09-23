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

        self.text_delay = 140
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
                            return "You recieve an egg."
                    case 1:
                        if dialogue_type == "start":
                            return "Use mouse to aim your first shot, fire with enter or left mouse click. Hold r to restart"
                        elif dialogue_type == "won":
                            return "WOW! Looks like somebody's getting the hang of things"

                    case 2:
                        if dialogue_type == "start":
                            return "If you get stuck, you can hold a to re-align yourself"
                        elif dialogue_type == "won":
                            return "Each level has a bullet count and time completed bonus objective, giving you a coin"

                    case 3:
                        if dialogue_type == "start":
                            "Have enough coins and you'll earn some gun Skins"
                        elif dialogue_type == "won":
                            "Well done! You've mastered the basics"

                    case 4:
                        if dialogue_type == "start":
                            return "I'm sure you can guess what will happen if you colide with those spikes"
                        elif dialogue_type == "won":
                            return "Good Job!"

                    case 5:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 6:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered spike avoidance"

                    case 7:
                        if dialogue_type == "start":
                            return "Something blocks the way, how could you remove this barrier?"
                        elif dialogue_type == "won":
                            return ""

                    case 8:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 9:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered using buttons."

                    case 10:
                        if dialogue_type == "start":
                            return "Maybe a slower approach could help you"
                        elif dialogue_type == "won":
                            return ""

                    case 11:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 12:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered time slow"

                    case 13:
                        if dialogue_type == "start":
                            return "Magasine's looking a little low? Mabye restock"
                        elif dialogue_type == "won":
                            return ""

                    case 14:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 15:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered magazine reload"

                    case 16:
                        if dialogue_type == "start":
                            return "Ever heard of portal, if so you know what to do"
                        elif dialogue_type == "won":
                            return ""

                    case 17:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 18:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered portals"

                    case 19:
                        if dialogue_type == "start":
                            return "What goes down, must come up. Or so I'm told"
                        elif dialogue_type == "won":
                            return ""

                    case 20:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 21:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered gravity swap"

                    case 22:
                        if dialogue_type == "start":
                            return "Seems that time is broken"
                        elif dialogue_type == "won":
                            return ""

                    case 23:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 24:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered time stop"

                    case 25:
                        if dialogue_type == "start":
                            return "Try using a bulet to clear a path"
                        elif dialogue_type == "won":
                            return ""

                    case 26:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 27:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered breakable surfaces"

                    case 28:
                        if dialogue_type == "start":
                            return "Small steps for big goals"
                        elif dialogue_type == "won":
                            return ""

                    case 29:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 30:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered mini coins"

                    case 31:
                        if dialogue_type == "start":
                            return "Shoot to kill, and to beat the stage"
                        elif dialogue_type == "won":
                            return ""

                    case 32:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 33:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered murder"

                    case 34:
                        if dialogue_type == "start":
                            return "This will mess with you head I'm sure"
                        elif dialogue_type == "won":
                            return ""

                    case 35:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 36:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered rotation reverse"

                    case 37:
                        if dialogue_type == "start":
                            return "Aim and fire, to your next destination"
                        elif dialogue_type == "won":
                            return ""

                    case 38:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 39:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Well done! You've mastered teleportation bullets"

                    case 40:
                        if dialogue_type == "start":
                            return "Your bullets could become incopereal"
                        elif dialogue_type == "won":
                            return ""

                    case 41:
                        if dialogue_type == "start" or dialogue_type == "won":
                            return ""

                    case 42:
                        if dialogue_type == "start":
                            ""
                        elif dialogue_type == "won":
                            "Congratulations! You've mastered ghost bullets"

                    case 43:
                        if dialogue_type == "start":
                            return "Nothing new anymore, your in the homestretch"
                        elif dialogue_type == "won":
                            return ""

                    case 44:
                        if dialogue_type == "start":
                            return "These levels should be your biggest challenge yet"
                        elif dialogue_type == "won":
                            return ""

                    case 45:
                        if dialogue_type == "start":
                            "Well done! You've mastered the abilities from the last three levels."
                        elif dialogue_type == "won":
                            ""

                    case 46:
                        if dialogue_type == "start":
                            return "5 to go"
                        elif dialogue_type == "won":
                            return ""

                    case 47:
                        if dialogue_type == "start":
                            return "4 more"
                        elif dialogue_type == "won":
                            return ""

                    case 48:
                        if dialogue_type == "start":
                            return "Final 3"
                        elif dialogue_type == "won":
                            ""

                    case 49:
                        if dialogue_type == "start":
                            return "The Penultimate Level"
                        elif dialogue_type == "won":
                            return ""

                    case 50:
                        if dialogue_type == "start":
                            return "NOTE IDK IF THIS IS POSSIBLE, IT's AN EXPERIMENT"
                        elif dialogue_type == "won":
                            return "HOWWW?"

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

        if self.text == "":
            self.active = False
            return

        screen.blit(self.image, self.rect)

    def display_text(self):

        if not self.active:
            return

        current_time = pygame.time.get_ticks()

        if self.word_index < len(self.word_list) and current_time - self.last_word_time >= self.text_delay:
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




        

import pygame
pygame.mixer.init()


button_fx = pygame.mixer.Sound("Game/Sounds/button_pressed.mp3")

gun_fired_fx = pygame.mixer.Sound("Game/Sounds/bullet_fired.mp3")

crash_fx = pygame.mixer.Sound("Game/Sounds/crash.mp3")

win_fx = pygame.mixer.Sound("Game/Sounds/win_fx.mp3")

man_ogg = pygame.mixer.Sound("Game/Sounds/Man_music.ogg")

laugh = pygame.mixer.Sound("Game/Sounds/Nelson_2.mp3")

new_voice_blip = pygame.mixer.Sound("Game/Sounds/new_voice_blip.mp3")


start_music = True

def play_music():

    pygame.mixer.music.load("Game/Sounds/human_music.mp3")

    pygame.mixer.music.play(-1)



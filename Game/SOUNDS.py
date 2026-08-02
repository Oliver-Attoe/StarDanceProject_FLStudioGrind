import pygame


button_fx = pygame.mixer.Sound("Sounds/button_pressed.mp3")
gun_fired_fx = pygame.mixer.Sound("Sounds/bullet_fired.mp3")
start_music = True
def play_music():
    pygame.mixer.music.load("Sounds/human_music.mp3")
    pygame.mixer.music.play(-1)

import pygame


button_fx = pygame.mixer.Sound("Sounds/button_pressed.mp3")
gun_fired_fx = pygame.mixer.Sound("Sounds/bullet_fired.mp3")
crash_fx = pygame.mixer.Sound("Sounds/crash.mp3")
win_fx = pygame.mixer.Sound("Sounds/win_fx.mp3")
man_ogg = pygame.mixer.Sound("Sounds/Man_music.ogg")
laugh = pygame.mixer.Sound("Sounds/Nelson_2.mp3")
voice_blip = pygame.mixer.Sound("Sounds/voice_blip.mp3")


start_music = True

def play_music():
    pygame.mixer.music.load("Sounds/human_music.mp3")
    pygame.mixer.music.play(-1)

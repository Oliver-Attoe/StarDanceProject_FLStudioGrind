
import pygame
pygame.mixer.init()


button_fx = pygame.mixer.Sound("Game/Sounds/button_pressed.mp3")

gun_fired_fx = pygame.mixer.Sound("Game/Sounds/bullet_fired.mp3")

crash_fx = pygame.mixer.Sound("Game/Sounds/crash.mp3")

win_fx = pygame.mixer.Sound("Game/Sounds/win_fx.mp3")

man_ogg = pygame.mixer.Sound("Game/Sounds/Man_music.ogg")

laugh = pygame.mixer.Sound("Game/Sounds/Nelson_2.mp3")

new_voice_blip = pygame.mixer.Sound("Game/Sounds/new_voice_blip.mp3")

bullet_pick_up_fx = pygame.mixer.Sound("Game/Sounds/ammo_pickup.mp3")

time_stop_fx = pygame.mixer.Sound("Game/Sounds/time_stop.mp3")

slow_time_fx = pygame.mixer.Sound("Game/Sounds/slow time.MP3")

up_gravity_fx = pygame.mixer.Sound("Game/Sounds/up.MP3")
up_gravity_fx.set_volume(1)
down_gravity_fx = pygame.mixer.Sound("Game/Sounds/and down.MP3")
down_gravity_fx.set_volume(1)

break_fx = pygame.mixer.Sound("Game/Sounds/broken_crate.mp3")

death_fx = pygame.mixer.Sound("Game/Sounds/death sound.mp3")


start_music = True

def play_music():

    pygame.mixer.music.load("Game/Sounds/human_music.mp3")

    pygame.mixer.music.play(-1)



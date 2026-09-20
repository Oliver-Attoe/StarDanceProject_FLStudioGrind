import pygame
from UI import timer_text


class Stopwatch:
    def __init__(self):
        super().__init__()
        self.running = False
        self.time_passed = 0
        self.start_time = None
        self.end_time = None
        self.milli = 0
        self.seconds = 0
        self.pause_start = None
        self.total_paused_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True


    def stop(self):
        self.end_time = pygame.time.get_ticks()
        self.running = False

    def reset_time(self):
        self.running = False
        self.time_passed = 0
        self.start_time = None
        self.end_time = None
        self.milli = 0
        self.seconds = 0
        self.pause_start = None
        self.total_paused_time = 0




    def display_timer(self, screen):


        self.seconds = int((self.time_passed / 1000) % 60)
        self.milli = self.time_passed % 1000

        timer_text_render = timer_text.render(
            f"{self.seconds}:{self.milli:03}",
            True,
            "Green"
        )

        timer_text_rect = timer_text_render.get_rect(center=(600, 75))
        screen.blit(timer_text_render, timer_text_rect)


    def update(self):
        if self.running:
                self.time_passed = (
                    pygame.time.get_ticks()
                    - self.start_time
                    - self.total_paused_time
                )

    def pause(self):
        if self.running:
           self.pause_start = pygame.time.get_ticks()


    def resume(self):
        if self.pause_start is not None:
            self.total_paused_time += pygame.time.get_ticks() - self.pause_start
            self.pause_start = None



    
        

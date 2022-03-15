import pygame
from settings import *

class SoundPlayer():
    def __init__(self,name):
        self.sound_dict = sound_dict
        self.sound = pygame.mixer.Sound(self.sound_dict[name])
        self.sound.set_volume(0.05)
        self.sound.play()

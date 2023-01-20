import pygame
import wave


class sprite():
    def __init__(self, image, sound_file):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.orig_sound_file = sound_file
        self.mod_sound_file = sound_file
        self.location = (100,200)
    
    def get_image(self):
        return self.image
    def set_image(self, new_image):
        self.image = pygame.image.load(new_image)
    def get_rect(self):
        return self.rect

    def get_sound(self):
        return self.orig_sound_file
    def set_sound(self, new_file):
        self.mod_sound_file = new_file
    
    def play_sound(self):
        #TODO make sprites play .wav file stored in mod_sound_file
        #this method should be triggered on click
        return 0
    
    def move(self):
        #TODO move sprites
        return 0
    


    

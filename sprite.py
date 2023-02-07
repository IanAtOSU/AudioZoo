import pygame


class sprite():
    volume = 1
    pitch = 1
    speed = 1

    width = 90
    height = 90

    def __init__(self, image, sound_file):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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

    def get_orig_sound(self):
        return self.orig_sound_file
    def get_mod_sound(self):
        return self.mod_sound_file
    def set_sound(self, new_file):
        self.mod_sound_file = new_file
    
    def play_sound(self):
        #TODO make sprites play .wav file stored in mod_sound_file
        #this method should be triggered on click
        return 0
    
    def scale(self, width, height):
        #TODO move sprites
        # Reese Clifford: Added a function to change the size of sprites

        # Uses the transform module that pygame provides to resize the image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()


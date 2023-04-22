import sys
import os
import pygame
import math
import tkinter.filedialog
from PIL import Image
import imghdr

import audio_functions

class audio_sprite():
    def __init__(self, image_file="Sprites/boxdude.png", sound_file="Sounds/Meme/metalgear.wav", width = 90, height = 90, initPos=(100,200)):

        self.initPos = initPos
        self.width = width
        self.height = height
        
        self.image_file = image_file
        self.image = pygame.transform.scale(pygame.image.load(self.image_file), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.orig_sound_file = sound_file
        self.mod_sound_file = sound_file

        self.volume = 0.5
        self.pitch = 0.5 
        self.speed = 0.5
        self.frame = 0


        self.looping = 0 #0 = not looping; -1 = is looping
        # RC: Added Code
        self.sound = pygame.mixer.Sound(self.mod_sound_file)
        self.playing = False

        self.key = pygame.key.key_code("g")

    def play(self):
        if not self.playing:
            self.sound = pygame.mixer.Sound(self.mod_sound_file)
            self.sound.play(loops=self.looping) 
            if self.looping == -1:
                self.playing = True

    def dance(self):
        if self.frame == 7:
            self.frame = 0
        else:
            self.frame += 1
        temp = self.image_file.split('/')
        temp[2] = str(self.frame) + ".png"
        newName = temp[0] + '/' + temp[1] + '/' + temp[2]

        self.image = pygame.transform.scale(pygame.image.load(newName), (self.width, self.height))


    def folderCheck(self):
        folder = self.image_file.split('/')
        if folder[0] == "SpriteFrames":
            return True
        else:
            return False


    def stop(self):
        if self.playing:
            self.sound.stop()
            self.playing = False
        
    def update_mod_sound_file(self):
        self.mod_sound_file = self.orig_sound_file
        if self.volume != 0.5:
            self.mod_sound_file = audio_functions.changeVolume(self.mod_sound_file, id(self),  self.volume)
        if self.pitch != 0.5:
            self.mod_sound_file = audio_functions.changePitch(self.mod_sound_file, id(self), self.pitch)
        if self.speed != 0.5:
            self.mod_sound_file = audio_functions.changeSpeed(self.mod_sound_file, id(self), self.speed)

    def saveState(self, curX, curY):
        ret = (str(curX)+","+str(curY)+","+str(self.width)+","+str(self.height)
               +","+str(self.image_file)+","+str(self.orig_sound_file)
               +","+str(self.volume)+","+str(self.pitch)+","+str(self.speed)+","+str(self.frame)+"\n")
        return ret

    def __del__(self):
        None


class slider():
    def __init__(self, screen, name="", minX=1400-410, maxX=1400-10, y=800-20,color=(115,105,215),slidercolor=[0,200,50]):
        if minX > maxX or minX < 0 or maxX > 900:
            ValueError
        self.name=name
        self.y = y
        self.minX = minX
        self.maxX = maxX
        self.x = minX + (maxX - minX) / 2
        self.color=color
        self.slidercolor=slidercolor
        self.screen = screen

    def get_level(self):
        #return (self.x - self.minX) / ((self.maxX-self.minX )/ self.levels[1]) + self.levels[0]
        return (self.x - self.minX) / ((self.maxX-self.minX ))

    def set_level(self, val):
        if val > 1 or val < 0:
            ValueError
        self.x = (val * (self.maxX - self.minX)) + self.minX

    def draw(self):
        pygame.draw.rect(self.screen, "Black", (self.minX-2, self.y-12, self.maxX - self.minX+4, 24) )
        pygame.draw.rect(self.screen, self.color, (self.minX, self.y-10, self.maxX - self.minX, 20) )
        pygame.draw.rect(self.screen, "Black", (self.minX+10, self.y-1, self.maxX - self.minX -20 , 1) )
        self.rect = pygame.draw.circle(self.screen, "Black", (self.x, self.y), 10)
        pygame.draw.circle(self.screen, self.slidercolor, (self.x, self.y), 9)


class textBox:
    def __init__(self, name, font, screen, x=0,y=0,width=100,height=20,background=(115,105,215),border=(0,0,0),textcolor=(0,0,0),text=""):
        self.name=name
        self.x=x
        self.y = y
        self.width = width
        self.height = height
        self.background=background
        self.border=border
        self.textcolor=textcolor
        self.text=text
        self.font=font
        self.screen = screen
    def draw(self):
        self.rect = pygame.draw.rect(self.screen,self.background,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(self.screen,self.border,(self.x,self.y,self.width,self.height),width=1)
        text_surface=self.font.render(self.text,False,self.textcolor)
        text_rect=text_surface.get_rect(center=(self.x+self.width/2,self.y+self.height/2))
        self.screen.blit(text_surface,text_rect)

    def within(self,x,y):
        return x>=self.x and x<=self.x+self.width and y>=self.y and y<=self.y+self.height

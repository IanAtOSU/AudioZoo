import sys
import os
import pygame
from abc import ABC, abstractmethod

import random


#If mixer glitches and gives you an error like "pygame.error: Failed loading libmpg123-0.dll: The specified module could not be found." try finding your pygame directory and adding something like the below
#os.add_dll_directory("C://Users/mrper_ssam80a/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
pygame.init()
pygame.mixer.init()
pygame.font.init()
game_font=pygame.font.SysFont("Times New Roman",30)

class sprite():
    def __init__(self, image="Sprites/sprite0.gif", sound_file="Sounds/metalgear.mp3", width = 30, height = 30, location=(100,200)):
        self.location = location
        self.width = width
        self.height = height
        
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

        self.orig_sound_file = sound_file
        self.mod_sound_file = sound_file

        self.volume = 1
        self.pitch = 1
        self.pitch=1
        self.speed=1

class slider():
    def __init__(self, minX=200, maxX=600, y=700):
        if minX > maxX or minX < 0 or maxX > 900:
            RuntimeError
        self.y = y
        self.minX = minX
        self.maxX = maxX
        self.x = minX + (maxX - minX) / 2

    def get_level(self):
        return self.x - ((self.maxX - self.minX) / 2)

class button(ABC):
    def __init__(self,name="",locationsize=(0,0,100,20),background=(255,255,255),border=(0,0,0),textcolor=(0,0,0),text=""):
        self.name=name
        self.locationsize=locationsize
        self.background=background
        self.border=border
        self.textcolor=textcolor
        self.text=text
    def draw(self):
        pygame.draw.rect(screen,self.background,self.locationsize)
        self.rect = pygame.draw.rect(screen,self.border,self.locationsize,width=1)
        text_surface=game_font.render(self.text,False,self.textcolor)
        screen.blit(text_surface,(self.locationsize[0],self.locationsize[1]))
        pygame.display.flip()
    def within(self,x,y):
        return x>=self.locationsize[0] and x<=self.locationsize[0]+self.locationsize[2] and y>=self.locationsize[1] and y<=self.locationsize[1]+self.locationsize[3]
    
    @abstractmethod
    def click():
        pass

#set up screen
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)
BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (1000,700))

#Create some sprites for testing
sprites = [sprite("Sprites/sprite0.gif", "Sounds/TestAudio.wav"), sprite("Sprites/sprite1.gif")]
dragging = False
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite
mouse_x = 0
mouse_y = 0

#position buttoins and sliders
class add_sprite_button(button):
    def __init__(self, name="",locationsize=(0,0,100,20),background=(255,255,255),border=(0,0,0),textcolor=(0,0,0),text=""):
        super().__init__(name,locationsize,background,border,textcolor,text)
    def click():
        print("testing testing 123")

addSpriteButton = add_sprite_button("addSprite",(50,height-50,250,50),"Add a sprite"),
buttons = [addSpriteButton]

widgets = [slider(400, 600, 700)]


#start game code

selected_sprite = sprites[0]

def check_for_drag(): 
    global dragging, mouse_x, mouse_y, initmousepos, initspritepos, sprites
    tmp = None
    for i in range(len(sprites)-1,-1,-1):#play corresponding sound to sprite clicked on, prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            mouse_x,mouse_y=event.pos
            dragging = True
            initmousepos=[mouse_x,mouse_y]
            initspritepos=[sprites[i].rect.x,sprites[i].rect.y]
            tmp=sprites[i] #give the object clicked on top priority
            sprites.remove(tmp)
            sprites.append(tmp)
            break #only interact with the first sprite found
    return tmp

def drag_sprite(mouse_x, mouse_y):
    sprites[len(sprites)-1].rect.x = initspritepos[0]+mouse_x-initmousepos[0]#object being dragged is always the last one
    sprites[len(sprites)-1].rect.y = initspritepos[1]+mouse_y-initmousepos[1]

def check_button_clicked():
    for x in buttons:
        if x.rect.collidepoint(pygame.mouse.get_pos()):
            x
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_sprite = check_for_drag()
            check_button_clicked()
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if abs(mouse_x-initmousepos[0]) < 5 and abs(mouse_y-initmousepos[1]) < 5 and selected_sprite != None:
                pygame.mixer.Sound(sprites[i].mod_sound_file).play()
                sprites[len(sprites)-1].rect.x = initspritepos[0]
                sprites[len(sprites)-1].rect.y = initspritepos[1] 
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x,mouse_y = event.pos
            drag_sprite(mouse_x, mouse_y)
            
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))
    
    #Draw Sprites
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    
    #Draw Buttons

    addSpriteButton.draw()#buttons go over sprites
    pygame.display.flip()

    #Draw Sliders
    pygame.draw.circle(screen, 'Blue', (widgets[0].x, widgets[0].y), 5)
    pygame.draw.rect(screen, 'Grey', [widgets[0].minX, widgets[0].y, widgets[0].maxX - widgets[0].minX, 10])


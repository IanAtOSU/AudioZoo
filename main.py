import sys
import os
import pygame
import random
import tkinter as tk
from tkinter import filedialog


#If mixer glitches and gives you an error like "pygame.error: Failed loading libmpg123-0.dll: The specified module could not be found." try finding your pygame directory and adding something like the below
#os.add_dll_directory("C://Users/mrper_ssam80a/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
pygame.init()
pygame.mixer.init()
pygame.font.init()
game_font=pygame.font.SysFont("Times New Roman",30)


class sprite():
    def __init__(self, image="Sprites/sprite0.gif", sound_file="Sounds/metalgear.mp3", width = 90, height = 90, initPos=(100,200)):
        self.initPos = initPos
        self.width = width
        self.height = height
        
        self.image = pygame.transform.scale(pygame.image.load(image), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.orig_sound_file = sound_file
        self.mod_sound_file = sound_file

        self.volume = 1
        self.pitch = 1
        self.pitch = 1
        self.speed = 1

        # RC: Added Code
        self.sound = pygame.mixer.Sound(self.mod_sound_file)
        self.playing = False


        def __del__(self):
            print("deleted sprite with audio file: " + str(self.orig_sound_file))

    # RC: Added Code
    def play(self):
        if not self.playing:
            self.sound.play(loops=-1)
            self.playing = True

    # RC: Added Code
    def stop(self):
        if self.playing:
            self.sound.stop()
            self.playing = False

class slider():
    def __init__(self, minX=200, maxX=600, y=700):
        if minX > maxX or minX < 0 or maxX > 900:
            ValueError
        self.y = y
        self.minX = minX
        self.maxX = maxX
        self.x = minX + (maxX - minX) / 2

    def get_level(self):
        return self.x - ((self.maxX - self.minX) / 2)

    def draw(self):
        pygame.draw.rect(screen, "Black", (self.minX-2, self.y-12, self.maxX - self.minX+4, 24) )
        pygame.draw.rect(screen, "Grey", (self.minX, self.y-10, self.maxX - self.minX, 20) )
        pygame.draw.rect(screen, "Black", (self.minX+10, self.y-1, self.maxX - self.minX -20 , 1) )
        self.rect = pygame.draw.circle(screen, "Black", (self.x, self.y), 10)
        pygame.draw.circle(screen, "Red", (self.x, self.y), 9)

class textBox:
    def __init__(self,name="",locationsize=(0,0,100,20),background=(255,255,255),border=(0,0,0),textcolor=(0,0,0),text=""):
        self.name=name
        self.locationsize=locationsize
        self.background=background
        self.border=border
        self.textcolor=textcolor
        self.text=text
    def draw(self):
        self.rect = pygame.draw.rect(screen,self.background,self.locationsize)
        pygame.draw.rect(screen,self.border,self.locationsize,width=1)
        text_surface=game_font.render(self.text,False,self.textcolor)
        screen.blit(text_surface,(self.locationsize[0],self.locationsize[1]))
    def within(self,x,y):
        return x>=self.locationsize[0] and x<=self.locationsize[0]+self.locationsize[2] and y>=self.locationsize[1] and y<=self.locationsize[1]+self.locationsize[3]

#set up screen
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)
BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (1400,800))


sprites = [sprite("Sprites/baloon.png", "Sounds/bruh.mp3"), sprite("Sprites/Cactus.png", "Sounds/emergency.mp3")]
dragging_sprite = False
dragging_slider = False

initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite
mouse_x = 0
mouse_y = 0


#position sprites on screen.

#Create textbox for adding sprites
addSpriteButton = textBox(name="addSprite",locationsize=(100,height-50,250,50),text="Add a sprite")
#Remove a Sprite button
removeSpriteButton = textBox(name="removeSprite",locationsize=(500,height-50,250,50),text="Remove a sprite")

changeBackgroundButton = textBox(name="changeBackground",locationsize=(900,height-50,250,50),text="Change Background")


#Change the Background button
#changeBackgroundButton = textBox(name="changeBackground",locationsize=(600,height-50,250,50),text="Change Background")

#Create slider
volume_slider = slider(300, 700, 600)

buttons = [addSpriteButton, removeSpriteButton, changeBackgroundButton]
sliders = [volume_slider]

selected_sprite = sprites[0]

def check_for_drag(): 
    global dragging_sprite, dragging_slider, mouse_x, mouse_y, initmousepos, initspritepos, initsliderpos, sprites, sliders
    tmp = None
    for i in range(len(sprites)-1,-1,-1):#play corresponding sound to sprite clicked on, prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            mouse_x,mouse_y=event.pos
            dragging_sprite = True
            initmousepos=[mouse_x,mouse_y]
            initspritepos=[sprites[i].rect.x,sprites[i].rect.y]
            tmp=sprites[i] #give the object clicked on top priority
            sprites.remove(tmp)
            sprites.append(tmp)
            break #only interact with the first sprite found
    for i in range(len(sliders)-1,-1,-1):
        if sliders[i].rect.collidepoint(pygame.mouse.get_pos()):
            mouse_x,mouse_y=event.pos
            dragging_slider = True
            initmousepos=[mouse_x,mouse_y]
            initsliderpos=[sliders[i].rect.x,sliders[i].rect.y]
            tmp=sliders[i] #give the object clicked on top priority
            sliders.remove(tmp)
            sliders.append(tmp)
            break #only interact with the first sprite found
    return tmp

def drag_sprite(mouse_x, mouse_y):
    sprites[len(sprites)-1].rect.x = initspritepos[0]+mouse_x-initmousepos[0]
    sprites[len(sprites)-1].rect.y = initspritepos[1]+mouse_y-initmousepos[1]

def drag_slider(mouse_x):
    if mouse_x > sliders[len(sliders)-1].maxX:
        sliders[len(sliders)-1].x = sliders[len(sliders)-1].maxX
    elif mouse_x < sliders[len(sliders)-1].minX:
        sliders[len(sliders)-1].x = sliders[len(sliders)-1].minX
    else:
        sliders[len(sliders)-1].x = initsliderpos[0]+mouse_x-initmousepos[0]

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN: 
            selected_sprite = check_for_drag()
            if addSpriteButton.within(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                potentialsprites=os.listdir("Sprites")
                potentialsounds=os.listdir("Sounds")
                sprites.append(sprite("Sprites/"+potentialsprites[random.randint(0,len(potentialsprites)-1)],"Sounds/"+potentialsounds[random.randint(0,len(potentialsounds)-1)]))
            
            # Check if Change Background button is clicked
            if changeBackgroundButton.within(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                # Open file dialog to select png image file
                filepath = filedialog.askopenfilename(initialdir="./Background", title="Select a background image", filetypes=[("PNG files", "*.png")])
                # Load the selected image file and scale it to the screen size
                if filepath:
                    BG = pygame.transform.scale(pygame.image.load(filepath), (width, height))


        elif event.type == pygame.MOUSEBUTTONUP: 
            if dragging_sprite:
                if removeSpriteButton.within(selected_sprite.rect.x, selected_sprite.rect.y):
                    del selected_sprite
                    sprites.remove(sprites[len(sprites)-1])
                dragging_sprite = False
            dragging_slider = False

            # RC: Added Code
            pos = pygame.mouse.get_pos()
            for sprite in sprites:
                if sprite.rect.collidepoint(pos):
                    if sprite.playing:
                        sprite.stop()
                    else:
                        sprite.play()

            if abs(mouse_x-initmousepos[0]) < 5 and abs(mouse_y-initmousepos[1]) < 5 and selected_sprite != None:
                pygame.mixer.Sound(sprites[i].mod_sound_file).play()
                sprites[len(sprites)-1].rect.x = initspritepos[0]
                sprites[len(sprites)-1].rect.y = initspritepos[1] 

        elif event.type == pygame.MOUSEMOTION: 

            mouse_x,mouse_y = event.pos
            if dragging_sprite:
                drag_sprite(mouse_x, mouse_y)
            if dragging_slider:
                drag_slider(mouse_x)

    
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))
    
    #Draw Sprites
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    
    #Draw Buttons
    for button in buttons:
        button.draw()
        
    #Draw Sliders
    for slider in sliders:
        slider.draw()

    pygame.display.flip()
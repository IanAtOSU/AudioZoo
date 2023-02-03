import sys
import os
import sprite, sliders
import pygame
import sprite
import random


#If mixer glitches and gives you an error like "pygame.error: Failed loading libmpg123-0.dll: The specified module could not be found." try finding your pygame directory and adding something like the below
#os.add_dll_directory("C://Users/mrper_ssam80a/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
pygame.init()
pygame.mixer.init()
pygame.font.init()
game_font=pygame.font.SysFont("Times New Roman",30)

class textBox:
    def __init__(self,name="",locationsize=(0,0,100,20),background=(255,255,255),border=(0,0,0),textcolor=(0,0,0),text=""):
        self.name=name
        self.locationsize=locationsize
        self.background=background
        self.border=border
        self.textcolor=textcolor
        self.text=text
    def draw(self):
        pygame.draw.rect(screen,self.background,self.locationsize)
        pygame.draw.rect(screen,self.border,self.locationsize,width=1)
        text_surface=game_font.render(self.text,False,self.textcolor)
        screen.blit(text_surface,(self.locationsize[0],self.locationsize[1]))
        pygame.display.flip()
    def within(self,x,y):
        return x>=self.locationsize[0] and x<=self.locationsize[0]+self.locationsize[2] and y>=self.locationsize[1] and y<=self.locationsize[1]+self.locationsize[3]

#set up screen
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)
BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (1000,700))

#Create a sprite
sprites = [sprite.sprite("Sprites/sprite0.gif", "Sounds/bruh.mp3"), sprite.sprite("Sprites/sprite1.gif", "Sounds/emergency.mp3")]
dragging = False
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite
mouse_x = 0
mouse_y = 0
sliders = [sliders.slider(700, 400, 600)]

#position sprites on screen.

#Create textbox for adding sprites
addSpriteButton=textBox(name="addSprite",locationsize=(50,height-50,250,50),text="Add a sprite")
buttons = [addSpriteButton]

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

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_sprite = check_for_drag()
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if abs(mouse_x-initmousepos[0]) < 5 and abs(mouse_y-initmousepos[1]) < 5 and selected_sprite != None:
                pygame.mixer.Sound(sprites[i].get_mod_sound()).play()
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
    for button in buttons:
        button.draw()#buttons go over sprites
    pygame.display.flip()

    #Draw Sliders
    pygame.draw.circle(screen, 'Blue', (sliders[0].x, sliders[0].y), 5)
    pygame.draw.rect(screen, 'Grey', [sliders[0].minX, sliders[0].y, sliders[0].maxX - sliders[0].minX, 10])


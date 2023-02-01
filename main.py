import sys, pygame
import os

import sprite
#If mixer glitches and gives you an error like "pygame.error: Failed loading libmpg123-0.dll: The specified module could not be found." try finding your pygame directory and adding something like the below
#os.add_dll_directory("C://Users/mrper_ssam80a/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
pygame.init()
pygame.mixer.init()

#set up screen
size = width, height = 800, 800
screen = pygame.display.set_mode(size)

#Create a sprite
sprites = [sprite.sprite("Sprites/sprite0.gif", "Sounds/bruh.mp3"), sprite.sprite("Sprites/sprite1.gif", "Sounds/emergency.mp3")]
dragging = False
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite
mouse_x = 0
mouse_y = 0
#position sprites on screen.

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
            sprites[len(sprites)-1].rect.x = initspritepos[0]+mouse_x-initmousepos[0]#object being dragged is always the last one
            sprites[len(sprites)-1].rect.y = initspritepos[1]+mouse_y-initmousepos[1]

    screen.fill((0,0,0))
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    pygame.display.flip()

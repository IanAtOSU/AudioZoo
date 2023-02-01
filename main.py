import sys, pygame
import os

import sprite, sliders
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

sliders = [sliders.slider(700, 400, 600)]

def check_sprite_clicked():
    global dragging, initmousepos, initspritepos
    tmp = None
    #mouse_x,mouse_y = 0
    for i in range(len(sprites)-1,-1,-1):#play corresponding sound to sprite clicked on, prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            mouse_x,mouse_y=event.pos
            dragging = True
            initmousepos=[mouse_x,mouse_y]
            initspritepos=[sprites[i].rect.x,sprites[i].rect.y]
            pygame.mixer.Sound(sprites[i].get_mod_sound()).play();
            tmp=sprites[i]#give the object clicked on top priority
            sprites.remove(tmp)
            sprites.append(tmp)
            break;#only interact with the first sprite found

def drag_sprite():
    mouse_x,mouse_y = event.pos
    sprites[len(sprites)-1].rect.x = initspritepos[0]+mouse_x-initmousepos[0]#object being dragged is always the last one
    sprites[len(sprites)-1].rect.y = initspritepos[1]+mouse_y-initmousepos[1]

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_sprite_clicked()
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            drag_sprite()
            
    screen.fill((0,0,0))
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)

    pygame.draw.circle(screen, 'Blue', (sliders[0].x, sliders[0].y), 5)
    pygame.draw.rect(screen, 'Grey', [sliders[0].minX, sliders[0].y, sliders[0].maxX - sliders[0].minX, 10])

    pygame.display.flip()

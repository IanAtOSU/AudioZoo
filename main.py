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
dragging = [False,0]
#position sprites on screen. 


#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(sprites)):#play corresponding sound to sprite clicked on
                if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
                    dragging = [True,i]
                    pygame.mixer.Sound(sprites[i].get_mod_sound()).play();
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging[0] = False
        elif event.type == pygame.MOUSEMOTION and dragging[0]:
            mouse_x,mouse_y = event.pos
            sprites[dragging[1]].rect.x = mouse_x
            sprites[dragging[1]].rect.y = mouse_y

    screen.fill((0,0,0))
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    pygame.display.flip()

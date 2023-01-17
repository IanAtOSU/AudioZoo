import sys, pygame
import os
#If mixer glitches and gives you an error like "pygame.error: Failed loading libmpg123-0.dll: The specified module could not be found." try finding your pygame directory and adding something like the below
#os.add_dll_directory("C://Users/mrper_ssam80a/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
pygame.init()
pygame.mixer.init()

#set up screen
size = width, height = 900, 900
screen = pygame.display.set_mode(size)

#create arrays of sprites
numSprites = 6;
sprites = [pygame.image.load("Sprites/sprite" + str(i) + ".gif") for i in range(numSprites)]
sprite_boxes = [x.get_rect() for x in sprites]

#add sounds corresponding to sprites
sounds=[];#list of sounds, at this point in same order as sprites
sounds.append(pygame.mixer.Sound("Sounds/bruh.mp3"))
sounds.append(pygame.mixer.Sound("Sounds/emergency.mp3"))
sounds.append(pygame.mixer.Sound("Sounds/mcoof.mp3"))
sounds.append(pygame.mixer.Sound("Sounds/metalgear.mp3"))
sounds.append(pygame.mixer.Sound("Sounds/soviet.mp3"))
sounds.append(pygame.mixer.Sound("Sounds/vine-boom.mp3"))

#position sprites on screen. 
#Currently just hardcoded for 6 sprites and 900x900 screen
for i in range(numSprites):
    if i<3:
        sprite_boxes[i] = sprite_boxes[i].move([50 + 200 * i,300])
    else:
        sprite_boxes[i] = sprite_boxes[i].move([50 + 200 * i - 600,600])


#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(sprites)):#play corresponding sound to sprite clicked on
                if sprite_boxes[i].collidepoint(pygame.mouse.get_pos()):
                    sounds[i].play();
            #for box in sprite_boxes:
            #    if box.collidepoint(pygame.mouse.get_pos()):
            #        screen.fill((0,0,0))

    screen.fill((0,0,0))
    for i in range(numSprites):
        screen.blit(sprites[i], sprite_boxes[i])
    pygame.display.flip()

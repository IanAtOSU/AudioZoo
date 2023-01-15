import sys, pygame
pygame.init()
pygame.mixer.init()

#set up screen
size = width, height = 900, 900
screen = pygame.display.set_mode(size)

#create arrays of sprites
numSprites = 6;
sprites = [pygame.image.load("sprite" + str(i) + ".gif") for i in range(numSprites)]
sprite_boxes = [x.get_rect() for x in sprites]

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
            for box in sprite_boxes:
                if box.collidepoint(pygame.mouse.get_pos()):
                    screen.fill((0,0,0))

    screen.fill((0,0,0))
    for i in range(numSprites):
        screen.blit(sprites[i], sprite_boxes[i])
    pygame.display.flip()
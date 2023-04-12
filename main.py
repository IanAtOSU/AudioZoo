import sys
import os
import pygame
import math
import tkinter.filedialog
from PIL import Image
import imghdr

#Our Files
import audio_functions
from classes import audio_sprite, slider, textBox

#pygame Initialization
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

#screen setup
clock = pygame.time.Clock()
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)

BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (width,height))

#sprite setup
sprites = [audio_sprite("SpriteFrames/duck/0.png", "Sounds/Drums/mixkit-drum-bass-hit-2294.wav"), audio_sprite("SpriteFrames/theCage/0.png", "Sounds/Flute/mixkit-game-flute-bonus-2313.wav")]
selected_sprite = sprites[0]

#dragging variables setup
dragging_sprite = False
dragging_slider = None
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite

#Textboxes, Buttons, and Sliders
game_font=pygame.font.SysFont("Times New Roman",30)
small_font=pygame.font.SysFont("Times New Roman",15)
#Create textbox for adding sprites
addSpriteButton = textBox(name="addSprite", font = game_font, screen = screen, x=1,y=height-50,width=250,height=50,text="Add a sprite")
#Remove a Sprite button
removeSpriteButton = textBox(name="removeSprite", font = game_font, screen = screen, x=251,y=height-50,width=250,height=50,text="Remove a sprite")
#Sprite looping button
loopSpriteButton = textBox(name="loopSprite", font = game_font, screen = screen, x=501,y=height-50,width=250,height=50,text="Looping: N")
#change background button
changeBGButton = textBox(name="changeBG", font = game_font, screen = screen, x=1, y= height-100, width= 250, height = 50, text = "Change background")
#key button binds sprite.play to different keyboard input
keyButton = textBox(name="changeKey", font = game_font, screen = screen, x=751, y= height-50, width= 75, height = 50, text = "g")
changeKeyNotif = textBox(name="changeKeyNotif", font = game_font, screen = screen, x=width/2-100, y= height/2-50, width= 200, height = 50, text = "Press any key")
#Reset sprite audio button
resetButton = textBox(name="reset", font = game_font,screen = screen, x=251, y = height-100, width = 250, height = 50, text = "Reset Sprite Audio")
#Duplicate sprite button
duplicateButton = textBox(name="duplicate", font = game_font, screen = screen, x=501, y= height-100, width= 250, height = 50, text = "Duplicate")


#Slider labels
volume_label = textBox(name="vol_lab", font = small_font,screen = screen, x=width-500,y=height-30,width=50,height=20,text="Volume")
pitch_label = textBox(name="pit_lab", font = small_font, screen = screen, x=width-500,y=height-55,width=50,height=20,text="Pitch")
speed_label = textBox(name="sped_lab", font = small_font, screen = screen, x=width-500,y=height-80,width=50,height=20,text="Speed")

#Create sliders
volume_slider = slider(screen, name="Volume",y=height-20)#previously(300, 700, 600)
pitch_slider = slider(screen, name="Pitch",y=height-45)
speed_slider = slider(screen, name="Speed",y=height-70)


buttons = [addSpriteButton, removeSpriteButton, changeBGButton,
            loopSpriteButton, volume_label,pitch_label,speed_label,
              resetButton, keyButton, duplicateButton]
sliders = [volume_slider,pitch_slider,speed_slider]

#Handles button clicks. x,y is given mousePosition
def clickButton(x, y):
    #Button click checks need to be first so they don't set selected_sprite to None
    #If add-a-sprite button is clicked
    global selected_sprite
    if addSpriteButton.within(x, y):
        image = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sprites\\")
        sound = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sounds\\")
        if image != '' and sound != '':
            sprites.append(audio_sprite(image_file=image, sound_file=sound))
    elif loopSpriteButton.within(x, y):
        if selected_sprite != None:
            if selected_sprite.looping == -1:
                selected_sprite.stop()
                selected_sprite.looping = 0
            else:
                selected_sprite.looping = -1
    elif changeBGButton.within(x, y):
        BG_temp = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Background\\")
        if BG_temp != '':
            BG = pygame.transform.scale(pygame.image.load(BG_temp), (1400,800))
    elif resetButton.within(x, y):
        if selected_sprite != None:
            for s in sliders:
                s.set_level(0.5)
            selected_sprite.volume = 0.5
            selected_sprite.pitch = 0.5
            selected_sprite.speed = 0.5
            selected_sprite.update_mod_sound_file()
    elif duplicateButton.within(x,y):
        if selected_sprite != None:
            dup_sprite = audio_sprite(image_file=selected_sprite.image_file, sound_file=selected_sprite.orig_sound_file, width = selected_sprite.width, height=selected_sprite.height)
            dup_sprite.volume = selected_sprite.volume
            dup_sprite.pitch = selected_sprite.pitch
            dup_sprite.speed = selected_sprite.speed
            dup_sprite.update_mod_sound_file()
            sprites.append(dup_sprite)
            selected_sprite = dup_sprite
        

    elif keyButton.within(x, y) and selected_sprite != None:
        flag=True
        while flag:
            changeKeyNotif.draw()
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYDOWN:
                    selected_sprite.key  = event2.key
                    flag = False

#loops through sprites, if a sprite is clicked, we return that sprite and set initspritepos and initmousepos apprpriately
def check_drag_sprite(): 
    global sprites, dragging_sprite, initmousepos, initspritepos
    tmp = None
    for i in range(len(sprites)-1,-1,-1):#prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            dragging_sprite = True
            initmousepos=[event.pos[0],event.pos[1]]
            initspritepos=[sprites[i].rect.x,sprites[i].rect.y]
            tmp=sprites[i] #give the object clicked on top priority
            sprites.remove(tmp)
            sprites.append(tmp)
            break #only interact with the first sprite found
    return tmp

#loops through sliders, if a slider is clicked, we return that slider and set initsliderpos and initmousepos appropriately 
def check_drag_slider():
    global sliders, dragging_slider, initmousepos, initsliderpos
    tmp = None
    for i in range(len(sliders)-1,-1,-1):
        if sliders[i].rect.collidepoint(pygame.mouse.get_pos()):
            dragging_slider = sliders[i]
            initmousepos=[event.pos[0],event.pos[1]]
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

#Measure bar setup
played_already = set([])
measure_stick = pygame.Rect(100, 4, 6, 160)

#sprite dancing setup (Make GIFs a directory of PNGs)
directory = './Sprites/'
gif_list = os.listdir(directory) #get names of files in sprites
os.chdir(directory) #into sprites directory ***DIR
for i in gif_list:
    if imghdr.what(i) == 'gif':
        filename = i
        temp = filename.split('.')
        dir_check = directory + temp[0]
        #check if directory with gif name exists
        if os.path.exists("../SpriteFrames/" + temp[0]):
            continue
        else:
            im = Image.open(i)
            os.chdir('../SpriteFrames') #into sprite frames directory ***DIR
            os.mkdir(temp[0]) 
            os.chdir("../SpriteFrames/" + temp[0]) #into new gif directory ***DIR
            for x in range(8):
                im.seek(im.n_frames // 8 * x)
                im.save('{}.png'.format(x)) # make 8 png files of gif
            im.close()
            os.chdir('../../Sprites') #back into /Sprites ***DIR

#change cwd back to home directory
os.chdir('../')



#game loop
while True:    
    #Update Button Text
    if selected_sprite == None:
        loopSpriteButton.text = "Looping: N/A"
        duplicateButton.text = "N/A"
        keyButton.text = "N/A"
    else:
        duplicateButton.text = "Duplicate"
        keyButton.text = pygame.key.name(selected_sprite.key)
        if selected_sprite.looping == -1: #-1 means is looping
            loopSpriteButton.text = "Looping: Y"
        else:
            loopSpriteButton.text = "Looping: N"
    
    #Update Slider levels
    if selected_sprite != None and dragging_slider == None:
        for i in sliders:
            if i == volume_slider:
                i.set_level(selected_sprite.volume)
            if i == pitch_slider:
                i.set_level(selected_sprite.pitch)
            if i == speed_slider:
                i.set_level(selected_sprite.speed)
    elif selected_sprite == None:
        for i in sliders:
            i.set_level(0.5)

    #Dancing Sprites
    for i in range(len(sprites)):
        if (sprites[i].looping == -1):
            if (sprites[i].folderCheck()):
                sprites[i].dance()
            continue
    
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            audio_functions.deleteOutfiles()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            
            #click buttons
            clickButton(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # There are 3 steps to dragging. 
            # 1. on MOUSEBUTTONDOWN, set selected_sprite/dragging_slider to what was clicked
            # 2. on MOUSEMOTION, if dragging then drag selected_sprite/dragging_slider from their inital positions (initspritepos/initsliderpos)
            # 3. on MOUSEBUTTONUP, we drop them into place and apply any effects from the drag (like removing sprites, changing volumes, etc)
            if (check_drag_slider() == None):
                selected_sprite = check_drag_sprite()
            if selected_sprite == None:
                dragging_slider = None
            
            
            
        elif event.type == pygame.MOUSEBUTTONUP: 

            #dragging
            if dragging_sprite:
                #If dragged under remove button
                if removeSpriteButton.within(selected_sprite.rect.x, selected_sprite.rect.y):
                    del selected_sprite
                    sprites.remove(sprites[len(sprites)-1])
                    selected_sprite = None
                dragging_sprite = False

            #If we dragged a slider
            if dragging_slider != None:
                if dragging_slider.name == "Volume":
                    selected_sprite.volume = dragging_slider.get_level()
                elif dragging_slider.name == "Pitch":
                    selected_sprite.pitch = dragging_slider.get_level()
                elif dragging_slider.name == "Speed":
                    selected_sprite.speed = dragging_slider.get_level()
                selected_sprite.update_mod_sound_file()

                dragging_slider = None
            #if sprite is clicked and NOT dragged
            elif abs(event.pos[0]-initmousepos[0]) < 5 and abs(event.pos[1]-initmousepos[1]) < 5 and selected_sprite != None:
                selected_sprite.play()
                sprites[len(sprites)-1].rect.x = initspritepos[0]
                sprites[len(sprites)-1].rect.y = initspritepos[1] 


        elif event.type == pygame.MOUSEMOTION:
            #dragging
            if dragging_sprite:
                drag_sprite(event.pos[0], event.pos[1])
            if dragging_slider != None:
                drag_slider(event.pos[0])

    #Play sprites with keystrokes
    for sprite in sprites:
        if pygame.key.get_pressed()[sprite.key]:
            sprite.play()

    #Draw Screen
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))

    #move measure stick
    pygame.draw.rect(screen, "Red", measure_stick)
    if measure_stick.x < width-20:
        measure_stick.x = measure_stick.x + 2
    else:
        measure_stick.x = 100
        if measure_stick.y <= (height-measure_stick.height-200):
            measure_stick.y += measure_stick.height+4
        else:
            measure_stick.y = 4
        played_already = set([]) #empty the played already list

    pygame.draw.rect(screen, "Black", pygame.Rect(100, 0, 10, height))

    #Draw Sprites
    for i in range(len(sprites)):
        if (sprites[i].rect.colliderect(measure_stick) and sprites[i] not in played_already):
            sprites[i].play()
            played_already.add(sprites[i])
        screen.blit(sprites[i].image, sprites[i].rect)

    #Draw selected sprite border
    if selected_sprite!=None:
        pygame.draw.rect(screen,(255,0,0),selected_sprite.rect,1,)
    
    #Draw Buttons
    for button in buttons:
        button.draw()
        
    #Draw Sliders
    for slider in sliders:
        slider.draw()

    clock.tick(60)

    pygame.display.flip()

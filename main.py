import sys
import os
import pygame
import math
import tkinter.filedialog
from PIL import Image
import imghdr
from datetime import datetime
import csv

#Our Files
import audio_functions
from classes import audio_sprite, slider, textBox

#pygame Initialization
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(100)
pygame.font.init()
clock = pygame.time.Clock()

#screen setup
clock = pygame.time.Clock()
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)

BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (width,height))

#sprite setup
sprites = [audio_sprite("SpriteFrames/baldmiles/0.png", "Sounds/Drums/mixkit-drum-bass-hit-2294.wav"), audio_sprite("SpriteFrames/balloon/0.png", "Sounds/Flute/mixkit-game-flute-bonus-2313.wav")]
selected_sprites = []
selected_sprites.append(sprites[0])

#dragging variables setup
dragging_sprite = False
dragging_slider = None
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be

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
#Save game button
saveButton = textBox(name="save", font = game_font, screen = screen, x=width-70, y= 1, width= 70, height = 50, text = "Save")
#Load game save button
loadButton = textBox(name="load", font = game_font, screen = screen, x=width-140, y= 1, width= 70, height = 50, text = "Load")


#Slider labels
volume_label = textBox(name="vol_lab", font = small_font,screen = screen, x=width-460,y=height-30,width=50,height=20,text="Volume")
pitch_label = textBox(name="pit_lab", font = small_font, screen = screen, x=width-460,y=height-55,width=50,height=20,text="Pitch")
speed_label = textBox(name="sped_lab", font = small_font, screen = screen, x=width-460,y=height-80,width=50,height=20,text="Speed")

#Create sliders
volume_slider = slider(screen, name="Volume",y=height-20) #previously(300, 700, 600)
pitch_slider = slider(screen, name="Pitch",y=height-45)
speed_slider = slider(screen, name="Speed",y=height-70)


buttons = [addSpriteButton, removeSpriteButton, changeBGButton,
            loopSpriteButton, volume_label,pitch_label,speed_label,
              resetButton, keyButton, duplicateButton,
              saveButton, loadButton]
sliders = [volume_slider,pitch_slider,speed_slider]

select_mult = False

#Handles button clicks. x,y is given mousePosition
def clickButton(x, y):
    #Button click checks need to be first so they don't set selected_sprites to None
    #If add-a-sprite button is clicked
    global selected_sprites, sprites, BG
    if addSpriteButton.within(x, y):
        image = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sprites\\")
        sound = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sounds\\")
        if image != '' and sound != '':
            sprites.append(audio_sprite(image_file=image, sound_file=sound))
    elif loopSpriteButton.within(x, y):
        if len(selected_sprites):
            for s in selected_sprites:
                if s.looping == -1:
                    s.stop()
                    s.looping = 0
                else:
                    s.looping = -1
    elif changeBGButton.within(x, y):
        BG_temp = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Background\\")
        if BG_temp != '':
            BG = pygame.transform.scale(pygame.image.load(BG_temp), (width,height))
    elif resetButton.within(x, y):
        if len(selected_sprites):
            for s in sliders:
                s.set_level(0.5)
            for s in selected_sprites:
                s.volume = 0.5
                s.pitch = 0.5
                s.speed = 0.5
                s.update_mod_sound_file()
    elif duplicateButton.within(x,y):
        if len(selected_sprites):
            new_selected_sprites = []
            for s in selected_sprites:
                dup_sprite = audio_sprite(image_file=s.image_file, sound_file=s.orig_sound_file, 
                                        width = s.width, height=s.height)
                dup_sprite.volume = s.volume
                dup_sprite.pitch = s.pitch
                dup_sprite.speed = s.speed
                dup_sprite.rect.x = s.rect.x + 8
                dup_sprite.rect.y = s.rect.y
                dup_sprite.update_mod_sound_file()
                sprites.append(dup_sprite)
                new_selected_sprites.append(dup_sprite)
            selected_sprites = new_selected_sprites
    elif saveButton.within(x,y):
        now = datetime.now()
        now = now.strftime("%Y-%m-%d-%H%M%S")
        spriteData=""
        write=True
        for s in sprites:
            if s.saveState(s.rect.x,s.rect.y):
                spriteData+=s.saveState(s.rect.x, s.rect.y)
            else:
                write=False
        if write:
            saveFile = open("SaveFiles/AudioZooSave"+str(now)+".csv", "w")
            saveFile.write(spriteData)
    elif loadButton.within(x,y):
        loadLocation = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\SaveFiles\\")
        if not loadLocation.endswith('.csv'):
            print(loadLocation)
            print("ERROR! INVALID SAVE FILE!")
        else:
            loadFile = open(loadLocation, "r")
            #9 commas
            for row in loadFile:
                spriteData = []
                ind = row.find(',')
                lastInd = ind+1
                spriteData.append(row[0:ind])
                #Import sprite data into array
                for _ in range(9):
                    ind = row.find(',', lastInd)
                    spriteData.append(row[lastInd:ind])
                    lastInd = ind+1
                #Correct types within array
                for i in range(4):
                    spriteData[i] = int(spriteData[i])
                for i in range(4, 6):
                    spriteData[i] = str(spriteData[i])
                for i in range(6, 9):
                    spriteData[i] = float(spriteData[i])
                #Generate new sprite
                newSprite = audio_sprite(image_file=spriteData[4], sound_file=spriteData[5])
                sprites.append(newSprite)
                #Fix sprite's data to match the loaded sprite
                newSprite.rect.x = spriteData[0]
                newSprite.rect.y = spriteData[1]
                newSprite.width = spriteData[2]
                newSprite.height = spriteData[3]
                newSprite.volume = spriteData[6]
                newSprite.pitch = spriteData[7]
                newSprite.speed = spriteData[8]
                newSprite.frame = spriteData[9]
                newSprite.update_mod_sound_file()
    elif removeSpriteButton.within(x, y):
        for s in selected_sprites:
            selected_sprites.remove(s)
            sprites.remove(s)
            del s


    elif keyButton.within(x, y) and len(selected_sprites):
        flag=True
        while flag:
            changeKeyNotif.draw()
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYDOWN:
                    for s in selected_sprites:
                        s.key  = event2.key
                        flag = False
    else:#no buttons clicked
        return False
    return True#some button clicked

#loops through sprites, if a sprite is clicked, we return that sprite and set sprites pre_drag_pos and initmousepos apprpriately
def check_drag_sprite(): 
    global sprites, dragging_sprite, initmousepos, select_mult
    if select_mult:
        tmp = selected_sprites
    else:
        tmp = []
    for i in range(len(sprites)-1,-1,-1):#prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            dragging_sprite = True
            initmousepos=[event.pos[0],event.pos[1]]
            sprites[i].pre_drag_pos = (sprites[i].rect.x, sprites[i].rect.y)
            tmp.append(sprites[i]) #give the object clicked on top priority
            sprites.remove(tmp[len(tmp)-1])
            sprites.append(tmp[len(tmp)-1])
            break #only interact with the first sprite found
        
    if tmp == [] and select_mult:
        tmp = selected_sprites
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
    for s in selected_sprites:
        s.rect.x = s.pre_drag_pos[0]+mouse_x-initmousepos[0]
        s.rect.y = s.pre_drag_pos[1]+mouse_y-initmousepos[1]

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
bar_moving=True

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
            for x in range(3):
                im.seek(im.n_frames // 3 * x)
                im.save('{}.png'.format(x)) # make 8 png files of gif
            im.close()
            os.chdir('../../Sprites') #back into /Sprites ***DIR
#change cwd back to home directory
os.chdir('../')

def sprite_dancing():
    global sprites
    for i in range(len(sprites)):	
        if (sprites[i].looping == -1):	
            if (sprites[i].folderCheck()):	
                sprites[i].buffer += 1	
                if sprites[i].buffer % 9 == 0:	
                    sprites[i].dance()	
            continue

#game loop
while True:    
    #Update Button Text
    if len(selected_sprites) == 0:
        loopSpriteButton.text = "Looping: N/A"
        duplicateButton.text = "N/A"
        keyButton.text = "N/A"
    else:
        duplicateButton.text = "Duplicate"
        keyButton.text = pygame.key.name(selected_sprites[len(selected_sprites)-1].key)
        if selected_sprites[len(selected_sprites)-1].looping == -1: #-1 means is looping
            loopSpriteButton.text = "Looping: Y"
        else:
            loopSpriteButton.text = "Looping: N"
    
	#Update Slider levels
    if len(selected_sprites) and dragging_slider == None:
        for i in sliders:
            if i == volume_slider:
                i.set_level(selected_sprites[len(selected_sprites)-1].volume)
            if i == pitch_slider:
                i.set_level(selected_sprites[len(selected_sprites)-1].pitch)
            if i == speed_slider:
                i.set_level(selected_sprites[len(selected_sprites)-1].speed)
    elif len(selected_sprites) == 0:
        for i in sliders:
            i.set_level(0.5)

    #Dancing Sprites	
    sprite_dancing()
    
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            audio_functions.deleteOutfiles()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            #click buttons
            clickButton(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # There are 3 steps to dragging. 
            # 1. on MOUSEBUTTONDOWN, set selected_sprites/dragging_slider to what was clicked
            # 2. on MOUSEMOTION, if dragging then drag selected_sprites/dragging_slider from their inital positions (pre_drag_pos/initsliderpos)
            # 3. on MOUSEBUTTONUP, we drop them into place and apply any effects from the drag (like removing sprites, changing volumes, etc)
            if (check_drag_slider() == None):
                selected_sprites = check_drag_sprite()
            if len(selected_sprites) == 0:
                dragging_slider = None
            
            
            
        elif event.type == pygame.MOUSEBUTTONUP: 
            #If we dragged a slider
            if dragging_slider != None:
                for s in selected_sprites:
                    if dragging_slider.name == "Volume":
                        s.volume = dragging_slider.get_level()
                    elif dragging_slider.name == "Pitch":
                        s.pitch = dragging_slider.get_level()
                    elif dragging_slider.name == "Speed":
                        s.speed = dragging_slider.get_level()
                    s.update_mod_sound_file()
                dragging_slider = None
            #if sprite is clicked and NOT dragged
            elif abs(event.pos[0]-initmousepos[0]) < 5 and abs(event.pos[1]-initmousepos[1]) < 5 and len(selected_sprites) >= 1:
                for s in selected_sprites:
                    s.play()
                    s.rect.x = s.pre_drag_pos[0]
                    s.rect.y = s.pre_drag_pos[1]
            #if a sprite was dragged
            else:
                for s in selected_sprites:
                    s.pre_drag_pos = (s.rect.x, s.rect.y)
            dragging_sprite = False


        elif event.type == pygame.MOUSEMOTION:
            #dragging
            if dragging_sprite:
                drag_sprite(event.pos[0], event.pos[1])
            if dragging_slider != None:
                drag_slider(event.pos[0])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bar_moving=(not bar_moving)
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL or event.key == pygame.K_LSHIFT:
                select_mult = True
            elif event.key == pygame.K_DELETE and len(selected_sprites):
                for s in selected_sprites:
                    sprites.remove(s)
                selected_sprites=[]
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL or event.key == pygame.K_LSHIFT:
                select_mult = False

    #Play sprites with keystrokes
    for sprite in sprites:
        if pygame.key.get_pressed()[sprite.key]:
            sprite.play()

    #Draw Screen
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))

    #move measure stick
    pygame.draw.rect(screen, "Red", measure_stick)
    if bar_moving:
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
        if (sprites[i].rect.colliderect(measure_stick) and sprites[i] not in played_already and bar_moving and not(sprites[i]==selected_sprites and dragging_sprite)):
            sprites[i].play()
            played_already.add(sprites[i])
        screen.blit(sprites[i].image, sprites[i].rect)
    #Draw selected sprite border
    if len(selected_sprites):
        for s in selected_sprites:
            pygame.draw.rect(screen,(255,0,0),s.rect,1)
    
    #Draw Buttons
    for button in buttons:
        button.draw()
        
    #Draw Sliders
    for slider in sliders:
        slider.draw()

    clock.tick(60)

    pygame.display.flip()

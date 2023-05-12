# AudioZoo
Like a zoo, but for sounds

AudioZoo is an audio manipulation game that makes creating music much more entertaining and rewarding than working with traditional audio editing software. Unlike many other music creation products, Audio Zoo is easy to understand and requires no previous experience with audio editing to get started. Colorful characters and backgrounds light up the screen, while Audio Zoo's modular and flexible design ensure that you can use it to create anything you can imagine! Beginners and teachers alike can benefit from this free and open source game that teaches the basics of audio manipulation.

# How to run AudioZoo youself
Developer Option:
1. navigate to the directory you wish to store audiozoo
2. git clone this github repo
3. use pip check/install to install any missing dependencies
4. Run the code with 'python main.py'

Traditional Option:
1. Download the latest release of AudioZoo (in the releases section of this project repository)
2. Unzip the contents
3. Run the AudioZoo.exe file

# How to use AudioZoo to create your own music
1. Add any necessary sound files to the AudioZoo/Sounds folder
    - AudioZoo comes preloaded with guitar, bass, flute, bell, and drum sounds.
    - The Sounds/Out/ folder is used for temporary storage of manipulated audio. Any Sounds stored here will be deleted on exit of the AudioZoo application
2. Add Sprites to the screen
    - click the 'add sprite' button. A file dialog will prompt you to select an image file (.jpg, .png, .gif) and an audio file (.wav)
    - After selecting both image and audio files, your new sprite will appear on screen
4. Play their audio by clicking their image, placing them in front of the measure bar, or pressing their assigned key-binding
    - Sprites will play only once per measure, or once per click
    - Every sprite has a default key-binding of 'g'
5. Select a Sprite by clicking or moving their image
    - Click the 'Loop' button to make their audio repeat after playing (again to stop playing)
    - Adjust their audio playback with the pitch/speed/volume sliders
    - Click the 'Reset Sprite Audio' button to reset their audio adjustments (pitch/speed/volume)
    - Click the 'Duplicate' button to create an identitcal copy of the selected sprite
    - Change their key-binding by clicking the 'change-key' button (default value shown as 'g' on screen)
    - Remove the sprite by pressing the 'delete' key, or dragging them over the 'Remove a Sprite' button
6. Select multiple sprites with 'ctrl + click'
    - All the options listed above are still available, their effect will apply to all sprites selected.
7. Arrange sprites to make songs with the measure bar, practice your piano skills with key presses, or just click sprites for fun
8. Once finished, be sure to click the 'save state' button to save all your progress
    - The state of the game will be stored in the AudioZoo/SaveFiles/ folder
    - To load a previously saved state, simply click the 'load state' button, which will prompt you to select a save file from which to load

# AudioZoo Libraries
AudioZoo uses two main python libraries, pygame and pydub.
- Pygame is used for rendering game GUI features (sprites, buttons, sliders, etc)
- Pydub is used for manipulating audio files, changing their speed, pitch, and volume.

A full working list of python libraries used in AudioZoo exists here:

    - Pygame
    - Pydub
    - numpy
    - PIL
    - imghdr
    - audioop
    - datetime
    - sys
    - os

# How to Contribute
Fork the Repository. It's completely open source!

Here is an architecture diagram to help better understand our code.
![image](https://github.com/TAssassinIT/AudioZoo/assets/37788709/3b331ca6-b970-4aaa-9ff1-2c53b1aa0b7d)

There are some helpful comments inside functions and classes that document intended functionality.
Also included is a unit_test.py, which executes some basic testing protocols.
Simply run unit_test.py inside the AudioZoo home directory with your favorite python compiler to test any modifications made.

We encourage anyone who is interested to contribute to this project!

# Future Development Roadmap
    - Compatability with more audio file formats (currently, only .wav is supported)
    - Export projects to audio files
    - More audio functions (such as reverb and reverse effects)
    - Improve user interface (such as dialog boxes for sprite settings instead of buttons)
    - Window resizing

# Credits/Acknowledgements
AudioZoo Team: Ian Tassin, Miles Wedemeyer, Andrew Saueran, Dillon Nguyen, Reece Clifford
Our Noble Project Partner: Alex Ulbrich

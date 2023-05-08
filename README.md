# AudioZoo
Like a zoo, but for sounds

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

# How to use AudioZoo to create your own music (Use-case Example)
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

# AudioZoo Build
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
Code format overview: Architecture Diagram
Future Development Roadmap

# Credits/Acknowledgements
AudioZoo Team: Ian Tassin, Miles Wedemeyer, Andrew Saueran, Dillon Nguyen, Reece Clifford
Our Noble Project Partner: Alex Ulbrich

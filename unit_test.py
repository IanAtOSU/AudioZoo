import unittest
from classes import audio_sprite, slider, textBox
import pygame
import time

pygame.init()
pygame.mixer.init()

class testSpriteMethods(unittest.TestCase):
    def setUp(self):
        self.sprite1 = audio_sprite()

    def test_sprite_setup(self):
        self.assertIsNotNone(self.sprite1.image_file)
        self.assertIsNotNone(self.sprite1.orig_sound_file)
        self.assertIsNotNone(self.sprite1.mod_sound_file)
        self.assertIsNotNone(self.sprite1.width)
        self.assertIsNotNone(self.sprite1.height)
    
    def test_play_audio(self):
        self.sprite1.play()
        self.assertEqual(self.sprite1.sound.get_num_channels(), 1)
        self.sprite1.stop()

    def test_looping(self):
        self.sprite1.looping = -1
        self.sprite1.play()
        time.sleep(self.sprite1.sound.get_length()+1)
        self.assertEqual(self.sprite1.sound.get_num_channels(), 1)
        self.sprite1.stop()

    def test_volume_change(self):
        before = self.sprite1.mod_sound_file
        self.sprite1.volume = 0.75
        self.sprite1.update_mod_sound_file()
        self.assertNotEqual(before, self.sprite1.mod_sound_file)
        self.sprite1.volume = 0.5
        self.sprite1.update_mod_sound_file()
        self.assertEqual(before, self.sprite1.mod_sound_file)

    def test_speed_change(self):
        before = self.sprite1.mod_sound_file
        self.sprite1.speed = 0.75
        self.sprite1.update_mod_sound_file()
        self.assertNotEqual(before, self.sprite1.mod_sound_file)
        self.sprite1.speed = 0.5
        self.sprite1.update_mod_sound_file()
        self.assertEqual(before, self.sprite1.mod_sound_file)

    def test_pitch_change(self):
        before = self.sprite1.mod_sound_file
        self.sprite1.pitch = 0.75
        self.sprite1.update_mod_sound_file()
        self.assertNotEqual(before, self.sprite1.mod_sound_file)
        self.sprite1.pitch = 0.5
        self.sprite1.update_mod_sound_file()
        self.assertEqual(before, self.sprite1.mod_sound_file)

    def test_all_audio_effects(self):
        before = self.sprite1.mod_sound_file
        self.sprite1.volume = 0.3
        self.sprite1.pitch = 0.85
        self.sprite1.speed = 0.65
        self.sprite1.update_mod_sound_file()
        self.assertNotEqual(before, self.sprite1.mod_sound_file, "Failed to update mod_sound_file")
        self.sprite1.volume = 0.5
        self.sprite1.pitch = 0.5
        self.sprite1.speed = 0.5
        self.sprite1.update_mod_sound_file()
        self.assertEqual(before, self.sprite1.mod_sound_file, "Failed to reset mod_sound_file")

    def test_sprite_duplication(self):
        dup_sprite = self.sprite1.duplicate()
        self.assertEqual(dup_sprite.mod_sound_file, self.sprite1.mod_sound_file)

    def test_nothing(self):
        pass

    def tearDown(self):
        del self.sprite1

if __name__ == '__main__':
    unittest.main()
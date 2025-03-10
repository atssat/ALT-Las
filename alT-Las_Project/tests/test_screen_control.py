# -*- coding: utf-8 -*-
import unittest
from screen_control import capture_screen

class TestScreenControl(unittest.TestCase):
    def test_capture_screen(self):
        img = capture_screen()
        self.assertIsNotNone(img)

if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
alT-Las Projesi
Ekran kontrol modülü.
Geliştiriciler: Özgür ve Vahap
"""
import pyautogui
import time
from PIL import Image
import mss

confidence_level = 0.7

def capture_screen():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screen_data = sct.grab(monitor)
            return Image.frombytes("RGB", screen_data.size, screen_data.bgra, "raw", "BGRX")
    except Exception as e:
        print(f"Ekran görüntüsü alma hatası: {str(e)}")
        return None

def find_element(screenshot, element_name):
    global confidence_level
    try:
        location = pyautogui.locateCenterOnScreen(element_name, confidence=confidence_level)
        if location is not None:
            x, y = location
            return x, y
        else:
            print(f"Eleman bulunamadı: {element_name}. Güven düzeyi: {confidence_level}")
            return None, None
    except Exception as e:
        print(f"Eleman bulma hatası: {str(e)}")
        return None, None

def click_element(x, y):
    try:
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click()
        time.sleep(1)
    except Exception as e:
        print(f"Elemana tıklama hatası: {str(e)}")

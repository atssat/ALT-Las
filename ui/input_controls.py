import speech_recognition as sr
import mediapipe as mp
import cv2
import numpy as np
import threading
from queue import Queue
import logging

logger = logging.getLogger(__name__)

class InputController:
    def __init__(self):
        self.voice_recognizer = sr.Recognizer()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.command_queue = Queue()
        self.running = False
        
    def start(self):
        self.running = True
        threading.Thread(target=self._voice_loop, daemon=True).start()
        threading.Thread(target=self._gesture_loop, daemon=True).start()
        
    def _voice_loop(self):
        while self.running:
            try:
                with sr.Microphone() as source:
                    audio = self.voice_recognizer.listen(source)
                    text = self.voice_recognizer.recognize_google(audio)
                    self.command_queue.put(('voice', text))
            except Exception as e:
                logger.error(f"Voice recognition error: {e}")
                
    def _gesture_loop(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            try:
                ret, frame = cap.read()
                if ret:
                    results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    if results.multi_hand_landmarks:
                        self.command_queue.put(('gesture', results.multi_hand_landmarks))
            except Exception as e:
                logger.error(f"Gesture recognition error: {e}")

import cv2
import numpy as np
from mss import mss
from PIL import Image
import logging
from queue import Queue
from threading import Thread
import time

logger = logging.getLogger(__name__)

class ScreenCapture:
    def __init__(self):
        self.sct = mss()
        self.recording = False
        self._frame_queue = Queue(maxsize=300)  # 10 seconds at 30fps
        self._recording_thread = None
        
    def capture_screen(self, monitor=1):
        try:
            screenshot = self.sct.grab(self.sct.monitors[monitor])
            return Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        except Exception as e:
            logger.error(f"Screen capture error: {e}")
            return None
            
    def start_recording(self, output_path='screen_recording.mp4', fps=30, 
                       quality=23, codec='h264'):
        if self.recording:
            return False
            
        self.recording = True
        self._recording_thread = Thread(target=self._record_screen,
                                     args=(output_path, fps, quality, codec),
                                     daemon=True)
        self._recording_thread.start()
        return True
        
    def stop_recording(self):
        self.recording = False
        if self._recording_thread:
            self._recording_thread.join()
            
    def _record_screen(self, output_path, fps, quality, codec):
        try:
            frame = self.capture_screen()
            height, width = np.array(frame).shape[:2]
            
            # Use GPU acceleration if available
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                writer = cv2.cudacodec.createVideoWriter(
                    output_path, cv2.VideoWriter_fourcc(*codec), fps,
                    (width, height), quality
                )
            else:
                writer = cv2.VideoWriter(
                    output_path, cv2.VideoWriter_fourcc(*codec), fps,
                    (width, height)
                )
                
            start_time = time.time()
            frame_count = 0
            
            while self.recording:
                frame = self.capture_screen()
                if frame:
                    frame_array = np.array(frame)
                    writer.write(frame_array)
                    frame_count += 1
                    
                    # Maintain FPS
                    elapsed = time.time() - start_time
                    expected_frames = int(elapsed * fps)
                    if frame_count > expected_frames:
                        time.sleep(1/fps)
                        
            writer.release()
            
        except Exception as e:
            logger.error(f"Recording error: {e}")
            self.recording = False

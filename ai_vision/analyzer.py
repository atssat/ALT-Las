import cv2
import numpy as np
from PIL import Image, ImageDraw
import torch

class AIVisionAnalyzer:
    def __init__(self):
        self.model = None
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        except Exception as e:
            print(f"Failed to load AI vision model: {e}")
    
    def analyze_frame(self, frame):
        if self.model is None:
            return None, []
            
        results = self.model(frame)
        detections = results.pandas().xyxy[0]
        
        # Draw bounding boxes and labels
        annotated_frame = frame.copy()
        for idx, det in detections.iterrows():
            x1, y1, x2, y2 = int(det['xmin']), int(det['ymin']), int(det['xmax']), int(det['ymax'])
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"{det['name']} {det['confidence']:.2f}",
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated_frame, detections.to_dict('records')

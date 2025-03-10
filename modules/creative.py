import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random
import logging

logger = logging.getLogger(__name__)

class CreativeEffects:
    @staticmethod
    def matrix_effect(image: Image.Image) -> Image.Image:
        try:
            # Convert to grayscale and apply matrix-like effect
            gray = image.convert('L')
            matrix = Image.new('RGB', image.size, 'black')
            draw = ImageDraw.Draw(matrix)
            
            chars = "01"
            font_size = 10
            char_width = 8
            
            for y in range(0, image.height, font_size):
                for x in range(0, image.width, char_width):
                    char = random.choice(chars)
                    brightness = gray.getpixel((x, y))
                    color = (0, int(brightness * 0.7), 0)
                    draw.text((x, y), char, fill=color)
                    
            return matrix
        except Exception as e:
            logger.error(f"Matrix effect error: {e}")
            return image
            
    @staticmethod
    def portal_effect(image: Image.Image, intensity: float = 0.5) -> Image.Image:
        try:
            # Create portal-like swirl effect
            center = (image.width // 2, image.height // 2)
            max_dist = np.sqrt(center[0]**2 + center[1]**2)
            
            result = image.copy()
            pixels = result.load()
            
            for x in range(image.width):
                for y in range(image.height):
                    dx = x - center[0]
                    dy = y - center[1]
                    distance = np.sqrt(dx**2 + dy**2)
                    angle = np.arctan2(dy, dx) + intensity * (1 - distance/max_dist)
                    
                    new_x = int(center[0] + distance * np.cos(angle))
                    new_y = int(center[1] + distance * np.sin(angle))
                    
                    if 0 <= new_x < image.width and 0 <= new_y < image.height:
                        pixels[x, y] = image.getpixel((new_x, new_y))
                        
            return result.filter(ImageFilter.SMOOTH)
        except Exception as e:
            logger.error(f"Portal effect error: {e}")
            return image

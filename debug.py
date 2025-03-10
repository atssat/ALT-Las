import logging
import sys
import torch
import psutil
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='debug.log'
)

logger = logging.getLogger(__name__)

def check_system():
    """System check"""
    logger.info("Checking system configuration...")
    
    # Python version
    logger.info(f"Python version: {sys.version}")
    
    # CUDA check
    if torch.cuda.is_available():
        logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA version: {torch.version.cuda}")
    else:
        logger.warning("CUDA not available")
        
    # Memory info
    memory = psutil.virtual_memory()
    logger.info(f"Total memory: {memory.total / (1024**3):.2f} GB")
    logger.info(f"Available memory: {memory.available / (1024**3):.2f} GB")
    
    # Disk info
    disk = psutil.disk_usage('/')
    logger.info(f"Disk total: {disk.total / (1024**3):.2f} GB")
    logger.info(f"Disk free: {disk.free / (1024**3):.2f} GB")

def check_dependencies():
    """Check required packages"""
    logger.info("Checking dependencies...")
    
    try:
        import numpy
        logger.info(f"NumPy version: {numpy.__version__}")
    except ImportError:
        logger.error("NumPy not found")
        
    try:
        import cv2
        logger.info(f"OpenCV version: {cv2.__version__}")
    except ImportError:
        logger.error("OpenCV not found")
        
    # Add more dependency checks...

def main():
    logger.info("Starting debug checks...")
    
    check_system()
    check_dependencies()
    
    logger.info("Debug checks completed")

if __name__ == "__main__":
    main()

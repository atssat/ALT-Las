import os
import sys
import time
import importlib
import argparse
import logging

# Check for tkinter availability
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("Error: tkinter is not available.")
    print("On Linux, install with: sudo apt-get install python3-tk")
    print("On Windows, reinstall Python and check 'tcl/tk and IDLE' during installation")
    sys.exit(1)

# Configure base imports
import numpy as np
import json
import threading
import queue
from PIL import Image, ImageTk
import cv2

# Configure logging
logging.basicConfig(level=logging.DEBUG if '--debug' in sys.argv else logging.INFO)
logger = logging.getLogger(__name__)

# Fix system path for local modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import local modules with fallbacks
try:
    from modules.performance import get_cpu_usage, get_memory_usage
    from modules.cuda_helper import is_cuda_available
    from modules.screen_capture import ScreenCapture
    from modules.vision import VisionProcessor
    screen_capture = ScreenCapture()
except ImportError as e:
    logger.warning(f"Module import error: {e}")
    from modules.fallbacks import (
        dummy_cpu_usage as get_cpu_usage,
        dummy_memory_usage as get_memory_usage,
        dummy_cuda_available as is_cuda_available
    )
    screen_capture = None

# Fix AI vision import
try:
    from ai_vision.analyzer import AIVisionAnalyzer
except ImportError:
    logger.error("Failed to import AIVisionAnalyzer")
    class AIVisionAnalyzer:
        def __init__(self):
            self.model = None
        def analyze_frame(self, frame):
            return frame, []

# Optional dependencies with fallbacks
AUDIO_AVAILABLE = False
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    logger.warning("sounddevice module not found. Audio monitoring will be disabled.")
    logger.info("To enable audio monitoring, install sounddevice: pip install sounddevice")

PSUTIL_AVAILABLE = False
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    logger.warning("psutil module not found. Performance monitoring will be disabled.")
    logger.info("To enable performance monitoring, install psutil: pip install psutil")

MATPLOTLIB_AVAILABLE = False
PLOT_AVAILABLE = False
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
    PLOT_AVAILABLE = True
except ImportError:
    logger.warning("matplotlib module not found. Graphical monitoring will be simplified.")
    logger.info("To enable full monitoring, install matplotlib: pip install matplotlib")
    plt = None

def check_dependencies():
    required = {
        'numpy': 'numpy',
        'psutil': 'psutil',
        'matplotlib': 'matplotlib',
        'sounddevice': 'sounddevice',
        'pyautogui': 'pyautogui',
        'keyboard': 'keyboard',
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'mss': 'mss',
        'torch': 'torch'
    }
    
    missing = []
    for module, package in required.items():
        if module != 'tkinter':  # Skip tkinter check
            if importlib.util.find_spec(module) is None:
                missing.append(package)
    
    if missing:
        print("Missing required packages. Please install:")
        print("pip install " + " ".join(missing))
        sys.exit(1)

class PluginInterface:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
    
    def load_plugin(self, name: str, path: str):
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.plugins[name] = module
                return True
        except Exception as e:
            if '--debug' in sys.argv:
                logger.error(f"Plugin load error: {e}")
        return False

def setup_argparse():
    parser = argparse.ArgumentParser(description='ALT Las Script')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--monitor', action='store_true', help='Enable performance monitoring')
    parser.add_argument('--array-size', type=int, default=1000, help='Size of test array')
    return parser.parse_args()

def array_operations(size: int, debug: bool = False):
    try:
        arr = np.random.rand(size)
        if debug:
            logger.debug(f"Array shape: {arr.shape}")
            logger.debug(f"Array memory usage: {arr.nbytes / 1024:.2f} KB")
        return arr
    except Exception as e:
        logger.error(f"Array operation error: {e}")
        return None

class DebugInterface(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.audio_queue = queue.Queue() if AUDIO_AVAILABLE else None
        self.cpu_data = []
        self.mem_data = []
        self.ai_vision = AIVisionAnalyzer()
        self.is_recording_audio = False
        self.is_capturing_screen = False
        self.is_monitoring_vision = False
        self.setup_interface()
        
    def setup_interface(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # System Monitor Tab
        self.system_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.system_tab, text='System Monitor')
        self.system_tab.grid_columnconfigure(0, weight=1)
        
        if MATPLOTLIB_AVAILABLE:
            # CPU/Memory Graphs with matplotlib
            self.fig, (self.cpu_ax, self.mem_ax) = plt.subplots(2, 1, figsize=(6, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, self.system_tab)
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        else:
            # Simple text-based monitoring
            monitor_frame = ttk.Frame(self.system_tab)
            monitor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            self.cpu_label = ttk.Label(monitor_frame, text="CPU: 0%")
            self.cpu_label.grid(row=0, column=0, pady=5)
            
            self.mem_label = ttk.Label(monitor_frame, text="Memory: 0%")
            self.mem_label.grid(row=1, column=0, pady=5)
            
            self.history_text = tk.Text(monitor_frame, height=10, width=40)
            self.history_text.grid(row=2, column=0, pady=5)

        # Audio Monitor Tab
        self.audio_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.audio_tab, text='Audio Monitor')
        
        if AUDIO_AVAILABLE and PLOT_AVAILABLE:
            self.audio_fig, self.audio_ax = plt.subplots()
            self.audio_canvas = FigureCanvasTkAgg(self.audio_fig, self.audio_tab)
            self.audio_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            # Initialize audio plotting
            self.audio_line = None
            self.audio_ax.set_ylim(-1, 1)
            self.audio_ax.set_title('Audio Waveform')
        else:
            ttk.Label(self.audio_tab, 
                     text="Audio monitoring disabled.\nInstall required modules to enable.",
                     justify=tk.CENTER).grid(row=0, column=0, pady=20)
        
        # Add control buttons to Audio tab
        audio_controls = ttk.Frame(self.audio_tab)
        audio_controls.grid(row=1, column=0, pady=5)
        
        self.audio_start_btn = ttk.Button(audio_controls, text="Start Recording", 
                                        command=self.toggle_audio_recording)
        self.audio_start_btn.pack(side=tk.LEFT, padx=5)
        
        # Screen Capture Tab
        self.screen_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.screen_tab, text='Screen Capture')
        
        self.screen_label = ttk.Label(self.screen_tab)
        self.screen_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add control buttons to Screen Capture tab
        capture_controls = ttk.Frame(self.screen_tab)
        capture_controls.grid(row=1, column=0, pady=5)
        
        self.capture_start_btn = ttk.Button(capture_controls, text="Start Capture",
                                          command=self.toggle_screen_capture)
        self.capture_start_btn.pack(side=tk.LEFT, padx=5)
        
        # AI Vision Tab
        self.vision_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vision_tab, text='AI Vision Debug')
        
        # Split into visualization and info areas
        self.vision_tab.grid_columnconfigure(1, weight=1)
        self.vision_tab.grid_rowconfigure(0, weight=1)
        
        # Vision display area
        vision_frame = ttk.Frame(self.vision_tab)
        vision_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.vision_canvas = tk.Label(vision_frame)
        self.vision_canvas.pack(expand=True, fill='both')
        
        # Detection info area
        info_frame = ttk.LabelFrame(self.vision_tab, text="AI Analysis")
        info_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.detection_text = tk.Text(info_frame, height=20, width=40)
        self.detection_text.pack(expand=True, fill='both')
        
        # Add control buttons to AI Vision tab
        vision_controls = ttk.Frame(self.vision_tab)
        vision_controls.grid(row=1, column=0, pady=5)
        
        self.vision_start_btn = ttk.Button(vision_controls, text="Start AI Vision",
                                         command=self.toggle_ai_vision)
        self.vision_start_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings Tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text='Settings')
        
        # API Settings
        api_frame = ttk.LabelFrame(self.settings_tab, text="API Configuration")
        api_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # API Keys
        self.api_entries = {}
        api_services = ['OpenAI', 'DeepSeek', 'Google', 'Cohere', 'AI21Labs']
        
        for service in api_services:
            frame = ttk.Frame(api_frame)
            frame.grid(row=api_services.index(service), column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
            ttk.Label(frame, text=f"{service} API Key:").grid(row=0, column=0, sticky=tk.W)
            entry = ttk.Entry(frame, show="*")
            entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
            self.api_entries[service] = entry
        
        # Add API validation button
        api_controls = ttk.Frame(api_frame)
        api_controls.grid(row=len(api_services), column=0, pady=10)
        
        ttk.Button(api_controls, text="Validate APIs", 
                  command=self.validate_apis).pack(side=tk.LEFT, padx=5)
        
        # Feature Toggles
        toggle_frame = ttk.LabelFrame(self.settings_tab, text="Feature Toggles")
        toggle_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.toggles = {}
        features = ['Audio Monitoring', 'Screen Capture', 'System Monitoring', 'Debug Logging']
        
        for feature in features:
            var = tk.BooleanVar(value=True)
            self.toggles[feature] = var
            ttk.Checkbutton(toggle_frame, text=feature, variable=var).grid(row=features.index(feature), column=0, sticky=tk.W)
        
        # Save/Load Settings
        btn_frame = ttk.Frame(self.settings_tab)
        btn_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(btn_frame, text="Save Settings", command=self.save_settings).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Load Settings", command=self.load_settings).grid(row=0, column=1)
        
        # Status area with scrollbar
        self.status_frame = ttk.Frame(self.settings_tab)
        self.status_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.settings_tab.grid_columnconfigure(0, weight=1)
        
        self.scrollbar = ttk.Scrollbar(self.status_frame)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.status_text = tk.Text(self.status_frame, height=10, width=50,
                                 yscrollcommand=self.scrollbar.set)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.config(command=self.status_text.yview)
        
        # Configure frame
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start all monitoring threads"""
        self.running = True
        # System monitoring thread
        threading.Thread(target=self.update_system_graphs, daemon=True).start()
        # Audio monitoring thread
        if AUDIO_AVAILABLE:
            threading.Thread(target=self.update_audio_display, daemon=True).start()
        # Screen capture thread
        threading.Thread(target=self.update_screen_capture, daemon=True).start()
        # AI vision monitoring thread
        threading.Thread(target=self.update_vision_display, daemon=True).start()
    
    def update_system_graphs(self):
        while self.running:
            try:
                if self.toggles['System Monitoring'].get():
                    cpu = get_cpu_usage()
                    mem = get_memory_usage()
                    self.cpu_data.append(cpu)
                    self.mem_data.append(mem)
                    
                    if len(self.cpu_data) > 50:
                        self.cpu_data.pop(0)
                        self.mem_data.pop(0)
                    
                    if MATPLOTLIB_AVAILABLE:
                        self.cpu_ax.clear()
                        self.mem_ax.clear()
                        self.cpu_ax.plot(self.cpu_data)
                        self.mem_ax.plot(self.mem_data)
                        self.cpu_ax.set_title('CPU Usage %')
                        self.mem_ax.set_title('Memory Usage %')
                        self.canvas.draw()
                    else:
                        self.cpu_label.config(text=f"CPU: {cpu}%")
                        self.mem_label.config(text=f"Memory: {mem}%")
                        self.history_text.insert('1.0', f"CPU: {cpu}% | Memory: {mem}%\n")
                        # Keep only last 100 lines
                        self.history_text.delete('101.0', tk.END)
            except Exception as e:
                logger.error(f"System monitoring error: {e}")
                time.sleep(5)  # Wait before retrying
            time.sleep(1)
    
    def update_audio_display(self):
        if not AUDIO_AVAILABLE or not PLOT_AVAILABLE:
            return
            
        while self.running:
            try:
                if self.is_recording_audio and self.toggles['Audio Monitoring'].get():
                    def audio_callback(indata, frames, time, status):
                        if self.toggles['Audio Monitoring'].get():
                            self.audio_queue.put(indata.copy())
                    
                    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
                        while self.running:
                            try:
                                data = self.audio_queue.get(timeout=1)
                                if hasattr(self, 'audio_ax'):
                                    self.audio_ax.clear()
                                    self.audio_ax.plot(data)
                                    self.audio_ax.set_ylim(-1, 1)
                                    self.audio_ax.set_title('Audio Waveform')
                                    self.audio_canvas.draw()
                            except queue.Empty:
                                pass
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Audio monitoring error: {e}")
    
    def update_screen_capture(self):
        if not screen_capture:
            logger.warning("Screen capture module not available")
            return
            
        while self.running:
            try:
                if self.is_capturing_screen and self.toggles['Screen Capture'].get():
                    screen = screen_capture.capture()
                    if screen is not None:
                        img = Image.fromarray(screen)
                        img.thumbnail((400, 300))
                        photo = ImageTk.PhotoImage(img)
                        self.screen_label.configure(image=photo)
                        self.screen_label.image = photo
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Screen capture error: {e}")
    
    def update_vision_display(self):
        while self.running:
            try:
                if self.is_monitoring_vision and hasattr(self, 'vision_canvas'):
                    if screen_capture and hasattr(self, 'vision_canvas'):
                        screen = screen_capture.capture()
                        if screen is not None:
                            # Convert to cv2 format
                            frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
                            
                            # Get AI analysis
                            annotated_frame, detections = self.ai_vision.analyze_frame(frame)
                            
                            if annotated_frame is not None:
                                # Convert back to PhotoImage
                                image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                                image.thumbnail((640, 480))
                                photo = ImageTk.PhotoImage(image)
                                
                                self.vision_canvas.configure(image=photo)
                                self.vision_canvas.image = photo
                                
                                # Update detection info
                                self.detection_text.delete('1.0', tk.END)
                                if detections:
                                    for det in detections:
                                        info = f"Found: {det['name']}\n"
                                        info += f"Confidence: {det['confidence']:.2f}\n"
                                        info += f"Location: ({int(det['xmin'])}, {int(det['ymin'])}) to "
                                        info += f"({int(det['xmax'])}, {int(det['ymax'])})\n\n"
                                        self.detection_text.insert(tk.END, info)
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"AI Vision error: {e}")
    
    def save_settings(self):
        settings = {
            'api_keys': {name: entry.get() for name, entry in self.api_entries.items()},
            'toggles': {name: var.get() for name, var in self.toggles.items()}
        }
        with open('debug_settings.json', 'w') as f:
            json.dump(settings, f)
        messagebox.showinfo("Success", "Settings saved successfully")
    
    def load_settings(self):
        try:
            with open('debug_settings.json', 'r') as f:
                settings = json.load(f)
                for name, value in settings['api_keys'].items():
                    if name in self.api_entries:
                        self.api_entries[name].delete(0, tk.END)
                        self.api_entries[name].insert(0, value)
                for name, value in settings['toggles'].items():
                    if name in self.toggles:
                        self.toggles[name].set(value)
            messagebox.showinfo("Success", "Settings loaded successfully")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved settings found")
    
    def toggle_audio_recording(self):
        self.is_recording_audio = not self.is_recording_audio
        if self.is_recording_audio:
            self.audio_start_btn.configure(text="Stop Recording")
        else:
            self.audio_start_btn.configure(text="Start Recording")
            
    def toggle_screen_capture(self):
        self.is_capturing_screen = not self.is_capturing_screen
        if self.is_capturing_screen:
            self.capture_start_btn.configure(text="Stop Capture")
        else:
            self.capture_start_btn.configure(text="Start Capture")
            
    def toggle_ai_vision(self):
        self.is_monitoring_vision = not self.is_monitoring_vision
        if self.is_monitoring_vision:
            self.vision_start_btn.configure(text="Stop AI Vision")
        else:
            self.vision_start_btn.configure(text="Start AI Vision")
    
    def validate_apis(self):
        """Validate API keys and connections"""
        results = []
        for name, entry in self.api_entries.items():
            key = entry.get().strip()
            if not key:
                results.append(f"{name}: No API key provided")
                continue
                
            # Test API connection
            try:
                if name == 'OpenAI':
                    import openai
                    openai.api_key = key
                    # Quick test call
                    openai.Completion.create(model="text-davinci-003", prompt="test", max_tokens=5)
                    results.append(f"{name}: Connection successful")
                # Add other API validations here...
            except Exception as e:
                results.append(f"{name}: Connection failed - {str(e)}")
        
        # Show results
        messagebox.showinfo("API Validation Results", "\n".join(results))

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Main container
        self.container = ttk.Frame(self.root)
        self.container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        
        # Create widgets in top frame
        self.create_widgets()
        
        # Create status text area
        self.status_frame = ttk.Frame(self.container)
        self.status_frame.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.status_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add status text widget
        self.status_text = tk.Text(self.status_frame, height=5, width=50,
                                 yscrollcommand=self.scrollbar.set)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.status_text.yview)
        
        # Create debug interface in bottom frame
        self.debug_interface = DebugInterface(self.container)
        self.debug_interface.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Update row weights
        self.container.grid_rowconfigure(3, weight=1)
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("ALT Las Interface")
        self.root.geometry("800x600")
        self.center_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create GUI widgets"""
        try:
            button_frame = ttk.Frame(self.container)
            button_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
            
            ttk.Button(button_frame, text="Run Analysis", 
                      command=self.run_analysis).grid(row=0, column=0, padx=5)
            ttk.Button(button_frame, text="Check Performance", 
                      command=self.check_performance).grid(row=0, column=1, padx=5)
            
            # Add clear button for status text
            ttk.Button(button_frame, text="Clear Log", 
                      command=self.clear_status).grid(row=0, column=2, padx=5)
        except Exception as e:
            logger.error(f"Error creating widgets: {e}")
            messagebox.showerror("Error", f"Failed to create GUI: {e}")
    
    def clear_status(self):
        """Clear the status text area"""
        if hasattr(self, 'status_text'):
            self.status_text.delete('1.0', tk.END)
            
    def on_closing(self):
        """Handle window closing"""
        self.root.quit()
        
    def run_analysis(self):
        try:
            arr = array_operations(1000, debug=True)
            if arr is not None:
                self.status_text.insert(tk.END, f"Array analysis complete. Mean: {np.mean(arr):.2f}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def check_performance(self):
        try:
            cpu = get_cpu_usage()
            mem = get_memory_usage()
            cuda = is_cuda_available()
            self.status_text.insert(tk.END, f"CPU: {cpu}%\nMemory: {mem}%\nCUDA: {cuda}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    args = setup_argparse()
    plugin_interface = PluginInterface()
    
    if args.debug:
        logger.debug("Debug mode enabled")
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Script location: {os.path.abspath(__file__)}")
        if 'get_cpu_usage' in globals():
            logger.debug(f"CPU Usage: {get_cpu_usage()}%")
            logger.debug(f"Memory Usage: {get_memory_usage()}%")
        logger.debug(f"CUDA Available: {is_cuda_available() if 'is_cuda_available' in globals() else 'N/A'}")
        test_array = array_operations(args.array_size, debug=True)
        if test_array is not None:
            logger.debug(f"Array mean: {np.mean(test_array):.2f}")

    try:
        root = tk.Tk()
        app = AppGUI(root)
        logger.info("GUI initialized successfully")
        root.mainloop()
    except Exception as e:
        logger.error(f"Failed to start GUI: {e}")
        raise

if __name__ == "__main__":
    check_dependencies()
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        if '--debug' in sys.argv:
            raise
        sys.exit(1)

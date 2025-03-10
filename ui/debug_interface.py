from tkinter import ttk, messagebox
import tkinter as tk
from ..core.monitoring import SystemMonitor, AudioMonitor, ScreenMonitor
from ..core.vision import VisionAnalyzer
import logging
import threading
import time

logger = logging.getLogger(__name__)

class DebugInterface(ttk.Frame):
    """Debug interface module extracted from main file"""
    def __init__(self, parent):
        super().__init__(parent)
        self.system_monitor = SystemMonitor(self.update_system_stats)
        self.audio_monitor = AudioMonitor(self.update_audio_stats)
        self.screen_monitor = ScreenMonitor(self.update_screen_stats)
        self.vision_analyzer = VisionAnalyzer()
        self.setup_interface()
        self.start_monitoring()
        
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
        
        self.cpu_label = ttk.Label(self.system_tab, text="CPU: 0%")
        self.cpu_label.grid(row=0, column=0, pady=5)
        
        self.mem_label = ttk.Label(self.system_tab, text="Memory: 0%")
        self.mem_label.grid(row=1, column=0, pady=5)
        
        self.gpu_label = ttk.Label(self.system_tab, text="GPU: 0%")
        self.gpu_label.grid(row=2, column=0, pady=5)
        
        self.history_text = tk.Text(self.system_tab, height=10, width=40)
        self.history_text.grid(row=3, column=0, pady=5)
        
        # Audio Monitor Tab
        self.audio_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.audio_tab, text='Audio Monitor')
        
        # Screen Capture Tab
        self.screen_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.screen_tab, text='Screen Capture')
        
        self.screen_label = ttk.Label(self.screen_tab)
        self.screen_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
        self.system_monitor.start()
        self.audio_monitor.start()
        self.screen_monitor.start()
        threading.Thread(target=self.update_logs, daemon=True).start()
    
    def update_logs(self):
        while self.running:
            try:
                with open('debug.log', 'r') as f:
                    logs = f.read()
                    self.status_text.delete('1.0', tk.END)
                    self.status_text.insert(tk.END, logs)
            except Exception as e:
                logger.error(f"Log update error: {e}")
            time.sleep(2)
    
    def update_system_stats(self, cpu, mem, gpu_stats):
        self.cpu_label.config(text=f"CPU: {cpu}%")
        self.mem_label.config(text=f"Memory: {mem}%")
        self.gpu_label.config(text=f"GPU: {gpu_stats.get('gpu_util', 0)}%")
    
    def update_audio_stats(self, audio_data):
        # Implement audio stats update logic
        pass
    
    def update_screen_stats(self, screen_data):
        # Implement screen stats update logic
        pass
    
    def toggle_ai_vision(self):
        # Implement AI vision toggle logic
        pass
    
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

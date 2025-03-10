import os

def create_project_structure():
    """
    alT-Las projesinin temel yapılandırmasını oluşturur.
    Bu aşamada ana uygulama dosyaları, GUI, utils, logger, exceptions,
    screen_control ve ai_models klasöründeki temel dosyalar kurulacak.
    """
    proje_dizini = "alT-Las_Project"
    os.makedirs(proje_dizini, exist_ok=True)

    # Oluşturulacak alt dizinler
    dizinler = [
        "ai_models",
        "cpp_modules/screen_capture",  # C++ modülü için (ileride derlenecek)
        "tests"
    ]
    for dizin in dizinler:
        os.makedirs(os.path.join(proje_dizini, dizin), exist_ok=True)

    # Dosya içerikleri (Setup-1.py ile oluşturulacak ana dosyalar)
    dosyalar = {
        # Ana uygulama dosyası
        os.path.join(proje_dizini, "alT_Las.py"): r'''# -*- coding: utf-8 -*-
"""
alT-Las Projesi
Yapay Zeka Destekli Masaüstü Asistanı
Geliştiriciler: Özgür ve Vahap
Versiyon: Alpha 0.09
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading, asyncio, aiohttp, time, os, argparse

# Kendi modüllerimiz
from screen_control import capture_screen, find_element, click_element
from gui import GUI
from utils import load_config, save_config
from logger import setup_logging, log_info, log_error, log_debug, log_performance
from exceptions import APIError, ElementNotFoundError, ConfigError, AIResponseError

# AI modelleri
from ai_models.deepseek_ai import DeepSeekAI
from ai_models.google_ai import GoogleAI
from ai_models.openai_py import OpenAI
from ai_models.cohere_ai import CohereAI
from ai_models.ai21labs_ai import AI21LabsAI

# C++ modülünden ekran yakalama (örnek)
import cpp_modules.screen_capture.screen_capture as sc

class alT_Las:
    def __init__(self, debug_mode=False):
        self.version = "Alpha 0.09"
        self.debug_mode = debug_mode
        self.root = tk.Tk()
        self.root.title(f"alT-Las - {self.version}")

        # Konfigürasyon
        self.config = load_config()
        self.api_keys = self.config["api_keys"]
        self.api_settings = self.config["api_settings"]
        self.rapidapi_settings = self.config.get("rapidapi", {"api_key": "", "apis": {}})

        # RapidAPI ayarları yoksa oluştur.
        if "rapidapi" not in self.config:
            self.config["rapidapi"] = {"api_key": "", "apis": {}}

        self.setup_logging()
        self.cache = {}
        self.cache_timeout = 300  # 5 dakika

        # AI Modelleri
        self.ai_models = {}
        self.load_ai_models()
        self.selected_ai = tk.StringVar(value=list(self.ai_models.keys())[0] if self.ai_models else "")

        self.screen_data = None
        self.element_locations = {}

        # GUI, config ve RapidAPI arayüzü
        self.gui = GUI(self.root, list(self.ai_models.keys()), self.selected_ai,
                       self.send_message, self.config, self.rapidapi_settings)
        self.configUI()
        self.rapidAPIUI()
        self.center_window()
        self.root.mainloop()

    def load_ai_models(self):
        try:
            self.ai_models = {
                "DeepSeek": DeepSeekAI(self.api_keys.get("deepseek", ""), self.api_settings.get("deepseek", {})),
                "GoogleAI": GoogleAI(self.api_keys.get("googleai", ""), self.api_settings.get("googleai", {})),
                "OpenAI": OpenAI(self.api_keys.get("openai", ""), self.api_settings.get("openai", {})),
                "Cohere": CohereAI(self.api_keys.get("cohere", ""), self.api_settings.get("cohere", {})),
                "AI21Labs": AI21LabsAI(self.api_keys.get("ai21labs", ""), self.api_settings.get("ai21labs", {}))
            }
            if hasattr(self, "gui") and self.gui:
                self.gui.ai_models = self.ai_models.keys()
                self.gui.ai_model_menu["menu"].delete(0, "end")
                for model in self.ai_models:
                    self.gui.ai_model_menu["menu"].add_command(label=model, command=tk._setit(self.selected_ai, model))
        except Exception as e:
            log_error(f"AI modeller yüklenirken hata: {e}")
            messagebox.showerror("Hata", f"AI Modelleri Yüklenemedi: {e}")

    def send_message(self, message):
        threading.Thread(target=self.process_message_thread, args=(message,), daemon=True).start()

    def process_message_thread(self, message):
        try:
            if message in self.cache and time.time() - self.cache[message]["timestamp"] < self.cache_timeout:
                response = self.cache[message]["response"]
                log_info(f"Önbellekten yanıt: {response}")
                self.gui.display_message(response, "alT-Las (Cached)")
                return
            if "ekran görüntüsü al" in message.lower():
                self.capture_and_display_screen()
            elif "eleman bul" in message.lower():
                self.find_and_click_element()
            else:
                start_time = time.time()
                response = asyncio.run(self.get_ai_response(message))
                end_time = time.time()
                if self.debug_mode:
                    log_performance(f"API Yanıt Süresi: {end_time - start_time:.2f} saniye")
                self.cache[message] = {"response": response, "timestamp": time.time()}
                self.gui.display_message(response, "alT-Las")
        except Exception as e:
            self.gui.display_message(str(e), "alT-Las")
            log_error(f"Mesaj işlenirken hata: {e}")

    def capture_and_display_screen(self):
        try:
            self.gui.display_message("Ekran görüntüsü alınıyor...", "alT-Las")
            file_path = sc.capture_screen("screenshot.png")
            if file_path:
                self.screen_data = file_path
                self.gui.display_message(f"Ekran görüntüsü alındı: {file_path}", "alT-Las")
            else:
                self.gui.display_message("Ekran görüntüsü alınamadı.", "alT-Las")
        except Exception as e:
            messagebox.showerror("Hata", "Ekran görüntüsü alınırken hata oluştu.")
            log_error(str(e))

    def find_and_click_element(self):
        if self.screen_data is None:
            self.gui.display_message("Önce ekran görüntüsü almalısınız!", "alT-Las")
            return
        element_name = simpledialog.askstring("Eleman Arama", "Aramak istediğiniz elemanın adını girin (ör: button.png):", parent=self.root)
        if element_name:
            try:
                if element_name in self.element_locations:
                    x, y = self.element_locations[element_name]
                    self.gui.display_message(f"{element_name} önbellekten bulundu.", "alT-Las")
                else:
                    x, y = find_element(self.screen_data, element_name)
                    if x is not None and y is not None:
                        self.element_locations[element_name] = (x, y)
                        self.gui.display_message(f"{element_name} bulundu ve önbelleğe alındı.", "alT-Las")
                    else:
                        self.gui.display_message(f"{element_name} bulunamadı!", "alT-Las")
                        return
                click_element(x, y)
                self.gui.display_message(f"{element_name} tıklandı.", "alT-Las")
            except Exception as e:
                self.gui.display_message(f"Hata: {str(e)}", "alT-Las")
                log_error(f"Eleman bulma/tıklama hatası: {e}", exc_info=True)
        else:
            self.gui.display_message("Eleman arama iptal edildi.", "alT-Las")

    async def get_ai_response(self, message):
        selected_ai = self.selected_ai.get()
        log_info(f"Seçilen AI: {selected_ai}, Mesaj: {message}")
        if not selected_ai:
            return "Lütfen bir AI modeli seçin."
        model = self.ai_models.get(selected_ai)
        if not model:
            return "Geçersiz AI modeli."
        try:
            async with aiohttp.ClientSession() as session:
                response = await model.get_response(session, message)
                return response
        except APIError as e:
            log_error(f"API Hatası ({selected_ai}): {e}")
            return f"API Hatası: {e}"
        except Exception as e:
            log_error(f"Beklenmeyen Hata ({selected_ai}): {e}")
            return "Bilinmeyen bir hata oluştu."

    def save_config(self):
        try:
            new_api_keys = {}
            new_api_settings = {}
            for ai_name in ["DeepSeek", "GoogleAI", "OpenAI", "Cohere", "AI21Labs"]:
                new_api_keys[ai_name.lower()] = self.api_key_entries[ai_name].get()
                new_api_settings[ai_name.lower()] = {"endpoint": self.api_setting_entries[ai_name].get()}
            self.config["api_keys"] = new_api_keys
            self.config["api_settings"] = new_api_settings
            save_config(self.config)
            self.load_ai_models()
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi ve güncellendi.")
        except Exception as e:
            log_error(f"Config kaydetme hatası: {e}")
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken hata oluştu: {e}")

    def save_rapidapi_config(self):
        try:
            api_key = self.rapidapi_key_entry.get()
            apis = {}
            for name, details in self.added_apis.items():
                apis[name] = {"endpoint": details["endpoint_entry"].get()}
            self.config["rapidapi"] = {"api_key": api_key, "apis": apis}
            save_config(self.config)
            messagebox.showinfo("Başarılı", "RapidAPI ayarları kaydedildi.")
        except Exception as e:
            log_error(f"RapidAPI ayarlarını kaydetme hatası: {e}")
            messagebox.showerror("Hata", f"RapidAPI ayarları kaydedilirken hata oluştu: {e}")

    def rapidAPIUI(self):
        self.rapidapi_tab = ttk.Frame(self.gui.notebook)
        self.gui.notebook.add(self.rapidapi_tab, text="RapidAPI")
        ttk.Label(self.rapidapi_tab, text="RapidAPI Anahtarı:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.rapidapi_key_entry = ttk.Entry(self.rapidapi_tab, width=50, show="*")
        self.rapidapi_key_entry.insert(0, self.rapidapi_settings.get("api_key", ""))
        self.rapidapi_key_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        ttk.Button(self.rapidapi_tab, text="Kaydet", command=self.save_rapidapi_config).grid(row=0, column=2, padx=5, pady=5)
        self.added_apis = {}
        self.api_frame = ttk.Frame(self.rapidapi_tab)
        self.api_frame.grid(row=1, column=0, columnspan=3, pady=10)
        ttk.Button(self.rapidapi_tab, text="API Ekle", command=self.add_rapidapi_entry).grid(row=2, column=0, columnspan=3, pady=5)

    def add_rapidapi_entry(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("RapidAPI Ekle")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="API Adı:").grid(row=0, column=0, sticky=tk.W)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, sticky=tk.E)
        ttk.Label(dialog, text="Endpoint:").grid(row=1, column=0, sticky=tk.W)
        endpoint_entry = ttk.Entry(dialog)
        endpoint_entry.grid(row=1, column=1, sticky=tk.E)
        def ok_pressed():
            api_name = name_entry.get()
            if api_name:
                self.added_apis[api_name] = {"endpoint_entry": endpoint_entry}
                self.update_rapidapi_list()
                dialog.destroy()
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir API adı girin.")
        ttk.Button(dialog, text="Tamam", command=ok_pressed).grid(row=2, column=1, sticky=tk.E)
        ttk.Button(dialog, text="İptal", command=dialog.destroy).grid(row=2, column=0, sticky=tk.W)
    def update_rapidapi_list(self):
        for widget in self.api_frame.winfo_children():
            widget.destroy()
        row_num = 0
        for name, details in self.added_apis.items():
            ttk.Label(self.api_frame, text=f"Ad: {name}").grid(row=row_num, column=0, sticky=tk.W)
            ttk.Label(self.api_frame, text=f"Endpoint: {details['endpoint_entry'].get()}").grid(row=row_num, column=1, sticky=tk.W)
            ttk.Button(self.api_frame, text="Kaldır", command=lambda n=name: self.remove_rapidapi_entry(n)).grid(row=row_num, column=2)
            row_num += 1
    def remove_rapidapi_entry(self, api_name):
        if api_name in self.added_apis:
            del self.added_apis[api_name]
            self.update_rapidapi_list()
    def configUI(self):
      self.settings_tab = ttk.Frame(self.gui.notebook)
      self.api_key_labels = {}
      self.api_key_entries = {}
      self.api_setting_labels = {}
      self.api_setting_entries = {}
      ai_names = ["DeepSeek", "GoogleAI", "OpenAI", "Cohere", "AI21Labs"]
      current_row = 0
      for ai_name in ai_names:
        ttk.Label(self.settings_tab, text=f"{ai_name} API Anahtarı:").grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
        self.api_key_labels[ai_name] = ttk.Label(self.settings_tab, text=f"{ai_name} API Key:")
        api_key_entry = ttk.Entry(self.settings_tab, width=50, show="*")
        api_key_entry.insert(0, self.api_keys.get(ai_name.lower(), ""))
        api_key_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="e")
        self.api_key_entries[ai_name] = api_key_entry
        current_row += 1
        ttk.Label(self.settings_tab, text=f"{ai_name} API URL:").grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
        self.api_setting_labels[ai_name] = ttk.Label(self.settings_tab, text=f"{ai_name} API URL:")
        api_url_entry = ttk.Entry(self.settings_tab, width=50)
        api_url_entry.insert(0, self.api_settings[ai_name.lower()].get("endpoint", ""))
        api_url_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="e")
        self.api_setting_entries[ai_name] = api_url_entry
        current_row += 1
      save_config_button = ttk.Button(self.settings_tab, text="Ayarları Kaydet", command=self.save_config)
      save_config_button.grid(row=current_row, column=0, columnspan=2, pady=10)
      ttk.Button(self.settings_tab, text="Ekran Görüntüsü Al", command=self.capture_and_display_screen).grid(row=current_row + 1, column=0, columnspan=2, pady=5)
      ttk.Button(self.settings_tab, text="Eleman Bul ve Tıkla", command=self.find_and_click_element).grid(row=current_row + 2, column=0, columnspan=2, pady=5)
      self.gui.notebook.add(self.settings_tab, text="Ayarlar")
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def setup_logging(self):
      log_level = __import__("logging").DEBUG if self.debug_mode else __import__("logging").INFO
      from logger import setup_logging
      setup_logging(log_level=log_level, log_file="AuraAI.log")
      log_info("Aura AI başlatılıyor...")
      if self.debug_mode:
            log_debug("Debug modu aktif.")
    def on_ai_model_changed(self, *args):
        selected_model = self.selected_ai.get()
        log_info(f"AI modeli değişti: {selected_model}")
        self.gui.display_message(f"AI Modeli: {selected_model} Seçildi.", "Bilgi")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="alT-Las Yapay Zeka Asistanı")
    parser.add_argument("--debug", action="store_true", help="Debug modunu etkinleştir")
    args = parser.parse_args()
    app = alT_Las(debug_mode=args.debug)
''',

    # Utils modülü
    os.path.join(proje_dizini, "utils.py"): r'''# -*- coding: utf-8 -*-
"""
alT-Las Projesi
Yardımcı fonksiyonlar modülü.
Geliştiriciler: Özgür ve Vahap
"""
import json
import os
import logging

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_keys": {
        "deepseek": "",
        "googleai": "",
        "openai": "",
        "cohere": "",
        "ai21labs": ""
    },
    "api_settings": {
        "deepseek": {"endpoint": "https://api.deepseek.com/v1/chat/completions", "model": "deepseek-chat"},
        "googleai": {"endpoint": ""},
        "openai": {"endpoint": ""},
        "cohere": {"endpoint": ""},
        "ai21labs": {"endpoint": ""}
    },
    "rapidapi": {
        "api_key": "",
        "apis": {}
    }
}

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return DEFAULT_CONFIG
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Konfigürasyon yükleme hatası: {e}. Varsayılan ayarlar kullanılıyor.")
        return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        logging.error(f"Konfigürasyon kaydetme hatası: {e}")
''',

    # Logger modülü
    os.path.join(proje_dizini, "logger.py"): r'''# -*- coding: utf-8 -*-
"""
alT-Las Projesi
Loglama modülü.
Geliştiriciler: Özgür ve Vahap
"""
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def setup_logging(log_level=logging.INFO, log_file=None):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=log_file,
        filemode='a' if log_file else 'w'
    )
    if log_file:
        logging.info(f"Log dosyası: {log_file}")
    else:
        logging.info("Konsola loglanıyor.")

def log_info(message):
    logging.info(message)

def log_error(message, exc_info=False):
    logging.error(message, exc_info=exc_info)

def log_debug(message):
    logging.debug(message)

def log_performance(message):
    logging.info(message)
''',

    # Exceptions modülü
    os.path.join(proje_dizini, "exceptions.py"): r'''# -*- coding: utf-8 -*-
"""
alT-Las Projesi
Özel hata sınıfları modülü.
Geliştiriciler: Özgür ve Vahap
"""
class APIError(Exception):
    pass

class ElementNotFoundError(Exception):
    pass

class ConfigError(Exception):
    pass

class AIResponseError(Exception):
    pass
''',

    # Screen Control modülü
    os.path.join(proje_dizini, "screen_control.py"): r'''# -*- coding: utf-8 -*-
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
'''
    }

    for dosya_yolu, icerik in dosyalar.items():
        dizin = os.path.dirname(dosya_yolu)
        os.makedirs(dizin, exist_ok=True)
        with open(dosya_yolu, "w", encoding="utf-8") as dosya:
            dosya.write(icerik)

    print("Setup-1.py: Proje yapısı ve temel dosyalar başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_project_structure()

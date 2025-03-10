# -*- coding: utf-8 -*-
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

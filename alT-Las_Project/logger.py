# -*- coding: utf-8 -*-
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

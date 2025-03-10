# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(message):
    logging.info(message)

def log_error(message, exc_info=False):
    logging.error(message, exc_info=exc_info)

def log_debug(message):
    logging.debug(message)

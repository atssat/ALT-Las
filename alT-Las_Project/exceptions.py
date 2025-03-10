# -*- coding: utf-8 -*-
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

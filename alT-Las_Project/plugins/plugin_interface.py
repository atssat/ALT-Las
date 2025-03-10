# -*- coding: utf-8 -*-
"""
Eklenti Yönetim Modülü
"""

class PluginInterface:
    def __init__(self):
        self.plugins = {}

    def load_plugin(self, plugin_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins[plugin_path] = module
            print(f"Eklenti yüklendi: {plugin_path}")
        except Exception as e:
            print(f"Eklenti yükleme hatası ({plugin_path}): {e}")

    def unload_plugin(self, plugin_path):
        if plugin_path in self.plugins:
            del self.plugins[plugin_path]
            print(f"Eklenti kaldırıldı: {plugin_path}")

    def list_plugins(self):
        return list(self.plugins.keys())

if __name__ == "__main__":
    pi = PluginInterface()
    print("Yüklü Eklentiler:", pi.list_plugins())

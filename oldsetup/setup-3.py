import os

def create_additional_files():
    project_root = "alT-Las_Project"
    
    # Ek dizinleri oluştur: plugins ve docs
    additional_dirs = [
        os.path.join(project_root, "plugins"),
        os.path.join(project_root, "docs")
    ]
    for d in additional_dirs:
        os.makedirs(d, exist_ok=True)
    
    # plugins/plugin_interface.py: Eklenti yönetimi için örnek arayüz
    plugin_interface_content = r'''# -*- coding: utf-8 -*-
"""
Plugin Interface modülü.
Bu modül, kullanıcının eklenti (plugin) ekleyebilmesine ve yönetebilmesine olanak tanır.
Geliştiriciler: Özgür ve Vahap
"""

class PluginInterface:
    def __init__(self):
        self.plugins = {}

    def load_plugin(self, plugin_path):
        """
        Belirtilen yol üzerinden eklentiyi yükler.
        Örneğin, Python modülü olarak import edilebilir.
        """
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
        """
        Yüklü eklentiyi kaldırır.
        """
        if plugin_path in self.plugins:
            del self.plugins[plugin_path]
            print(f"Eklenti kaldırıldı: {plugin_path}")
        else:
            print("Eklenti bulunamadı.")

    def list_plugins(self):
        """
        Yüklü eklentileri listeler.
        """
        return list(self.plugins.keys())

if __name__ == "__main__":
    pi = PluginInterface()
    print("Şu an yüklü eklentiler:", pi.list_plugins())
'''
    plugin_interface_path = os.path.join(project_root, "plugins", "plugin_interface.py")
    with open(plugin_interface_path, "w", encoding="utf-8") as f:
        f.write(plugin_interface_content)
print("Ek dosyalar.")
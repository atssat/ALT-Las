# ALT-Las

Yapay zeka destekli hata ayıklama ve izleme arayüzü.

## Özellikler

- Gerçek zamanlı sistem izleme
- Ses görselleştirme
- Ekran yakalama ve analiz
- Yapay zeka görüntü işleme
- Çoklu yapay zeka modeli desteği (OpenAI, Google AI, vb.)
- Eklenti sistemi
- Asenkron API yönetimi
- GPU izleme ve kaynak yönetimi
- Canlı güncellemeli hata ayıklama arayüzü
- Otomatik temizlemeli önbellek sistemi
- CI/CD entegrasyonu

## Kurulum

```bash
# Depoyu klonla
git clone https://github.com/atssat/ALT-Las.git
cd ALT-Las

# Sanal ortam oluştur
python -m venv .venv
.\.venv\Scripts\activate  # Windows için

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Kullanım

```bash
python alT_Las.py --debug
```

## Geliştirici Notları

1. **Gereksinimler**
   - Python 3.11 veya üstü
   - CUDA destekli ekran kartı (opsiyonel)
   - Windows 10/11

2. **Ortam Hazırlığı**
   - Sanal ortam oluşturun
   - Gereksinimleri yükleyin
   - API anahtarlarını ayarlayın

3. **Test ve Geliştirme**
   - Testleri çalıştırın: `.\run_tests.ps1`
   - Kod kalitesi kontrolü: `black . && pylint **/*.py`
   - Hata ayıklama modu: `python alT_Las.py --debug`

4. **Performans Optimizasyonu**
   - GPU kullanımı için CUDA ayarları
   - Bellek yönetimi optimizasyonları
   - API çağrıları önbellekleme

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

# Hata yonetimi
$ErrorActionPreference = "Stop"

function Install-Dependencies {
    param (
        [string]$requirement
    )
    try {
        Write-Host "Yukleniyor: $requirement..." -ForegroundColor Green
        pip install $requirement
        if ($LASTEXITCODE -ne 0) {
            throw "$requirement yuklenemedi"
        }
    }
    catch {
        Write-Host "Hata: $requirement yukleme hatasi: $_" -ForegroundColor Red
        return $false
    }
    return $true
}

# Sanal ortam olustur ve aktif et
Write-Host "Sanal ortam olusturuluyor..." -ForegroundColor Green
python -m venv .venv
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

.\.venv\Scripts\Activate.ps1

# pip'i guncelle
Write-Host "pip guncelleniyor..." -ForegroundColor Green
python -m pip install --upgrade pip wheel setuptools
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# ONNX kurulumu
Write-Host "ONNX yukleniyor..." -ForegroundColor Green
pip install --no-deps onnx==1.15.0
pip install --no-deps onnxruntime-gpu==1.16.3

# PyTorch'u CUDA destegi ile yukle
Write-Host "PyTorch CUDA destegi ile yukleniyor..." -ForegroundColor Green
pip install torch==2.6.0+cu118 torchvision==0.17.0+cu118 torchaudio==2.6.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
if ($LASTEXITCODE -ne 0) {
    Write-Host "CPU versiyonuna geciliyor..." -ForegroundColor Yellow
    pip install torch==2.6.0+cpu torchvision==0.17.0+cpu torchaudio==2.6.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
}

# Diger gereksinimleri yukle
Write-Host "Diger gereksinimler yukleniyor..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Kurulum tamamlandi!" -ForegroundColor Green

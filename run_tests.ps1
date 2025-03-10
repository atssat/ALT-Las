# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install or update dependencies
Write-Host "Installing/updating dependencies..." -ForegroundColor Green
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install test dependencies
Write-Host "Installing test dependencies..." -ForegroundColor Green
pip install pytest pytest-cov

# Verify critical dependencies
Write-Host "Verifying dependencies..." -ForegroundColor Green
python -c "import psutil, cv2, torch, numpy; print('Dependencies OK')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Critical dependencies missing" -ForegroundColor Red
    exit 1
}

# Run system checks
Write-Host "`nRunning system checks..." -ForegroundColor Green
python debug.py

# Run unit tests with retry
Write-Host "`nRunning unit tests..." -ForegroundColor Green
$maxRetries = 3
$retry = 0
do {
    python -m pytest tests/ -v --cov=./ --cov-report=xml
    if ($LASTEXITCODE -eq 0) { break }
    $retry++
    if ($retry -lt $maxRetries) {
        Write-Host "Retrying tests..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while ($retry -lt $maxRetries)

# Run performance tests if tests passed
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nRunning performance tests..." -ForegroundColor Green
    python -m cProfile -o profile.stats alT_Las.py --debug --monitor
}

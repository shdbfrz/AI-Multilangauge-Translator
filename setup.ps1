# Quick Setup Script for AI Multi-Language Translator

Write-Host "🌍 AI Multi-Language Translator Setup" -ForegroundColor Cyan
Write-Host "=====================================`n" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.7+ first." -ForegroundColor Red
    exit 1
}

# Check if pip is available
Write-Host "`n🔍 Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ Pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Pip not found. Please ensure pip is installed." -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "`n📦 Installing Python packages..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

try {
    pip install -r requirements.txt
    Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error installing packages. Please check your internet connection." -ForegroundColor Red
    Write-Host "You can try installing manually with:" -ForegroundColor Yellow
    Write-Host "pip install flask transformers torch langdetect speechrecognition gtts pyaudio" -ForegroundColor White
    exit 1
}

# Optional: Install PyAudio for voice input
Write-Host "`n🎤 Setting up voice input..." -ForegroundColor Yellow
Write-Host "Note: Voice input requires PyAudio. If installation fails, you can skip this feature." -ForegroundColor Yellow

try {
    pip install pyaudio
    Write-Host "✅ Voice input ready!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PyAudio installation failed. Voice input may not work." -ForegroundColor Yellow
    Write-Host "You can still use the translator without voice features." -ForegroundColor Yellow
}

Write-Host "`n🚀 Setup Complete!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host "To start the translator:" -ForegroundColor White
Write-Host "1. Run: python app.py" -ForegroundColor Cyan
Write-Host "2. Open: http://localhost:5000" -ForegroundColor Cyan
Write-Host "3. Start translating!" -ForegroundColor Cyan
Write-Host "`nNote: First translation may take longer as models download." -ForegroundColor Yellow

Write-Host "🚀 Starting NETGITS Quiz Setup Process..." -ForegroundColor Cyan

# 1. التحقق من وجود بايثون
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed on this system!" -ForegroundColor Red
    Write-Host "💡 Please download and install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Exit
}

# 2. إنشاء البيئة الوهمية
Write-Host "📦 Creating Python Virtual Environment (venv)..." -ForegroundColor Blue
python -m venv venv

# 3. تفعيل البيئة الوهمية
Write-Host "🔄 Activating Virtual Environment..." -ForegroundColor Blue
.\venv\Scripts\Activate.ps1

# 4. تثبيت المكتبات
Write-Host "⚙️ Installing dependencies from requirements.txt..." -ForegroundColor Blue
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. تشغيل التطبيق
Write-Host "✅ Setup successful! Launching source.py..." -ForegroundColor Green
python source.py

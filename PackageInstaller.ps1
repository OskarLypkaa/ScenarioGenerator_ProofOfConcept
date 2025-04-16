Write-Host "=== Installing Python dependencies ==="

# (Opcjonalnie) utwórz wirtualne środowisko
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Lista wymaganych paczek
$packages = @(
    "openai",
    "pyautogui",
    "pytesseract",
    "pywinauto",
    "pynput",
    "mss",
    "Pillow",
    "xlsxwriter",
    "pywin32"
)

foreach ($pkg in $packages) {
   Write-Host "📦 Installing $pkg ..."
   pip install $pkg
}

Write-Host "✅ All required packages have been installed."

@echo off
echo 🔨 Compilando ImageClicker Múltiple...
cd /d "%~dp0"

echo 📦 Activando entorno virtual...
call venv\Scripts\activate

echo 🛠️ Instalando dependencias...
pip install -r requirements.txt

echo 🏗️ Compilando con PyInstaller...
pyinstaller --onefile image_clicker\main.py --name ImageClickerMultiple --windowed --add-data "fotos;fotos"

echo ✅ Compilación completada!
echo 📁 El ejecutable está en: dist\ImageClickerMultiple.exe
pause

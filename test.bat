@echo off
echo 🧪 Probando ImageClicker Múltiple...
cd /d "%~dp0"

echo 📦 Activando entorno virtual...
call venv\Scripts\activate

echo 🔧 Instalando dependencias si no están...
pip install -r requirements.txt

echo 🚀 Ejecutando ImageClicker...
python image_clicker\main.py

pause

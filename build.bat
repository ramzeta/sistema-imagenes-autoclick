@echo off
cd /d "%~dp0"
venv\Scripts\activate
pyinstaller --onefile image_clicker\main.py --name ImageClicker --windowed
pause

@echo off
setlocal enabledelayedexpansion

echo =============================
echo  [*] Preparando entorno venv
echo =============================

IF NOT EXIST venv (
    echo [+] Creando entorno virtual...
    python -m venv venv
)

echo [+] Activando entorno...
call venv\Scripts\activate

echo =============================
echo  [*] Actualizando pip
echo =============================
python -m pip install --upgrade pip

echo =============================
echo  [*] Instalando dependencias
echo =============================
pip install -r requirements.txt
pip install pyinstaller

echo =============================
echo  [*] Verificando recursos
=============================
dir /b image_clicker\*.png >nul 2>nul
IF EXIST image_clicker\*.png (
    echo [+] Imágenes PNG detectadas.
) ELSE (
    echo [!] No se detectaron imágenes PNG en image_clicker\ (esto es opcional).
)

echo =============================
echo  [*] Generando ejecutable EXE
echo =============================
pyinstaller ImageClicker.spec

IF EXIST dist\ImageClicker.exe (
    echo =============================
    echo  [✓] Ejecutable creado con éxito
    echo =============================
) ELSE (
    echo =============================
    echo  [X] ERROR: El ejecutable no se generó.
    echo  Verifica los logs anteriores.
    echo =============================
)

pause

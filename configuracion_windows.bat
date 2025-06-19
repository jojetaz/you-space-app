@echo off
echo ========================================
echo CONFIGURACION PARA WINDOWS - YOU-SPACE.INFO
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo.
echo [2/5] Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo [3/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [4/5] Verificando base de datos...
python verificar_db.py

echo.
echo [5/5] Configuracion completada!
echo.
echo ========================================
echo INSTRUCCIONES PARA DESPLIEGUE:
echo ========================================
echo.
echo 1. Sube todos los archivos a tu servidor Linux
echo 2. Ejecuta en el servidor: bash deploy.sh
echo 3. Configura Cloudflare con tu IP del servidor
echo 4. Tu sitio estara en: https://you-space.info
echo.
echo ========================================
pause 
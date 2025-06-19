@echo off
echo Iniciando Portafolio de Herramientas IA (modo rapido)...

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    echo Instalando dependencias por primera vez...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Entorno virtual encontrado, activando...
    call venv\Scripts\activate.bat
    
    REM Verificar si las dependencias ya están instaladas
    python -c "import flask, flask_sqlalchemy, flask_login, flask_wtf, werkzeug, PIL, dotenv, email_validator" 2>nul
    if errorlevel 1 (
        echo Instalando dependencias faltantes...
        pip install -r requirements.txt
    ) else (
        echo Dependencias ya instaladas, saltando instalacion...
    )
)

REM Verificar si existe la carpeta tema y sus subcarpetas
if not exist "tema" (
    echo Creando estructura de carpetas del tema...
    mkdir tema
    mkdir tema\templates
    mkdir tema\assets
    mkdir tema\assets\uploads
)

REM Iniciar la aplicación
echo Iniciando la aplicacion...
python app.py

REM Mantener la ventana abierta
pause 
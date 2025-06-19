@echo off
echo Iniciando Portafolio de Herramientas IA...

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Verificar si existe la carpeta tema y sus subcarpetas
if not exist "tema" (
    echo Creando estructura de carpetas del tema...
    mkdir tema
    mkdir tema\templates
    mkdir tema\assets
    mkdir tema\assets\uploads
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Iniciar la aplicación
echo Iniciando la aplicación...
python app.py

REM Mantener la ventana abierta
pause 
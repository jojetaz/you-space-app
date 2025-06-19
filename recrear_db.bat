@echo off
echo Recreando base de datos...

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar el script de recreación
python recrear_db.py

REM Mantener la ventana abierta
pause 
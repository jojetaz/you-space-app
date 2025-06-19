@echo off
echo Actualizando base de datos...

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar el script de actualización
python actualizar_db.py

REM Mantener la ventana abierta
pause 
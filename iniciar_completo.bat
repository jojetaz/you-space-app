@echo off
echo Iniciando la aplicacion (modo completo)...
echo.

:: Activar el entorno virtual
call venv\Scripts\activate.bat

:: Ejecutar el script de inicio completo
python start.py

:: Mantener la ventana abierta si hay un error
pause 
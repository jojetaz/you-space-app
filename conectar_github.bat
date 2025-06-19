@echo off
echo ========================================
echo CONECTANDO CON GITHUB
echo ========================================
echo.

set /p username="Ingresa tu nombre de usuario de GitHub: "
if "%username%"=="" (
    echo ERROR: Debes ingresar tu nombre de usuario
    pause
    exit /b 1
)

echo.
echo [1/3] Añadiendo origen remoto...
git remote add origin https://github.com/%username%/you-space-app.git

echo.
echo [2/3] Cambiando rama a main...
git branch -M main

echo.
echo [3/3] Subiendo código a GitHub...
git push -u origin main

echo.
echo ========================================
echo ¡REPOSITORIO CONECTADO EXITOSAMENTE!
echo ========================================
echo.
echo Tu repositorio está en:
echo https://github.com/%username%/you-space-app
echo.
echo Próximo paso: Configurar Render.com
echo.
pause 
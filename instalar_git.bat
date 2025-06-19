@echo off
echo ========================================
echo INSTALANDO GIT AUTOMATICAMENTE
echo ========================================
echo.

echo [1/4] Descargando Git...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.50.0.windows.1/Git-2.50.0-64-bit.exe' -OutFile 'git-installer.exe'}"

if %errorlevel% neq 0 (
    echo ERROR: No se pudo descargar Git
    echo.
    echo ALTERNATIVA MANUAL:
    echo 1. Ve a: https://git-scm.com/download/win
    echo 2. Descarga Git para Windows
    echo 3. Instala con opciones por defecto
    pause
    exit /b 1
)

echo.
echo [2/4] Git descargado exitosamente
echo.

echo [3/4] Instalando Git...
echo Por favor, sigue las instrucciones del instalador:
echo - Click "Next" en todas las opciones
echo - Usa configuración por defecto
echo - Click "Install"
echo.
git-installer.exe /VERYSILENT /NORESTART

echo.
echo [4/4] Verificando instalacion...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo VERIFICANDO INSTALACION DE GIT
echo ========================================
echo.

git --version
if %errorlevel% equ 0 (
    echo.
    echo ✅ Git instalado correctamente!
    echo.
    echo Ahora puedes ejecutar:
    echo .\subir_a_github.bat
    echo.
) else (
    echo.
    echo ⚠️ Git no se detecto automaticamente
    echo.
    echo Por favor:
    echo 1. Cierra esta ventana
    echo 2. Abre una nueva ventana de PowerShell
    echo 3. Ejecuta: git --version
    echo 4. Si funciona, ejecuta: .\subir_a_github.bat
    echo.
)

echo ========================================
pause 
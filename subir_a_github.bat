@echo off
echo ========================================
echo SUBIENDO PROYECTO A GITHUB
echo ========================================
echo.

echo [1/4] Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git no esta instalado
    echo Descarga Git desde: https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo [2/4] Inicializando repositorio Git...
if not exist .git (
    git init
    echo Repositorio Git inicializado
) else (
    echo Repositorio Git ya existe
)

echo.
echo [3/4] Añadiendo archivos...
git add .
git status

echo.
echo [4/4] Creando commit...
set /p commit_msg="Mensaje del commit (Enter para usar mensaje por defecto): "
if "%commit_msg%"=="" set commit_msg="You-Space App - Configuracion inicial"

git commit -m "%commit_msg%"

echo.
echo ========================================
echo PROYECTO LISTO PARA SUBIR A GITHUB
echo ========================================
echo.
echo Ahora necesitas:
echo 1. Crear un repositorio en GitHub
echo 2. Seguir las instrucciones de GitHub
echo 3. Ejecutar: git remote add origin [URL_DEL_REPO]
echo 4. Ejecutar: git push -u origin main
echo.
echo ========================================
pause 
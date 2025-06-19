Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALANDO GIT CON POWERSHELL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/4] Verificando si Git ya está instalado..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✅ Git ya está instalado: $gitVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora puedes ejecutar: .\subir_a_github.bat" -ForegroundColor Cyan
        Read-Host "Presiona Enter para continuar"
        exit 0
    }
} catch {
    Write-Host "Git no está instalado, continuando con la instalación..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[2/4] Descargando Git..." -ForegroundColor Yellow
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.50.0.windows.1/Git-2.50.0-64-bit.exe"
$installerPath = "$env:TEMP\git-installer.exe"

try {
    Write-Host "Descargando desde: $gitUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $gitUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ Git descargado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al descargar Git" -ForegroundColor Red
    Write-Host ""
    Write-Host "ALTERNATIVA MANUAL:" -ForegroundColor Yellow
    Write-Host "1. Ve a: https://git-scm.com/download/win" -ForegroundColor Cyan
    Write-Host "2. Descarga Git para Windows" -ForegroundColor Cyan
    Write-Host "3. Instala con opciones por defecto" -ForegroundColor Cyan
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Instalando Git..." -ForegroundColor Yellow
Write-Host "Ejecutando instalador en modo silencioso..." -ForegroundColor Gray

try {
    Start-Process -FilePath $installerPath -ArgumentList "/VERYSILENT", "/NORESTART" -Wait
    Write-Host "✅ Instalación completada" -ForegroundColor Green
} catch {
    Write-Host "❌ Error durante la instalación" -ForegroundColor Red
    Write-Host "Intentando ejecutar instalador manualmente..." -ForegroundColor Yellow
    Start-Process -FilePath $installerPath
    Write-Host "Por favor, sigue las instrucciones del instalador" -ForegroundColor Cyan
    Read-Host "Presiona Enter cuando termine la instalación"
}

Write-Host ""
Write-Host "[4/4] Verificando instalación..." -ForegroundColor Yellow
Write-Host "Esperando 10 segundos para que se complete la instalación..." -ForegroundColor Gray
Start-Sleep -Seconds 10

# Refrescar variables de entorno
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✅ Git instalado correctamente: $gitVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 ¡Listo! Ahora puedes ejecutar:" -ForegroundColor Cyan
        Write-Host "   .\subir_a_github.bat" -ForegroundColor White
    } else {
        Write-Host "⚠️ Git no se detectó automáticamente" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Por favor:" -ForegroundColor Cyan
        Write-Host "1. Cierra esta ventana de PowerShell" -ForegroundColor White
        Write-Host "2. Abre una nueva ventana de PowerShell" -ForegroundColor White
        Write-Host "3. Ejecuta: git --version" -ForegroundColor White
        Write-Host "4. Si funciona, ejecuta: .\subir_a_github.bat" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Error al verificar Git" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Read-Host "Presiona Enter para continuar" 
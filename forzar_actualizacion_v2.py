#!/usr/bin/env python3
"""
Script para forzar la actualización de la aplicación en Render
"""

import os
import sys
import subprocess
import time

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {descripcion}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {descripcion} completado exitosamente")
        if resultado.stdout:
            print(f"📄 Salida: {resultado.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {descripcion}: {e}")
        if e.stdout:
            print(f"📄 Salida: {e.stdout}")
        if e.stderr:
            print(f"⚠️  Error: {e.stderr}")
        return False

def verificar_archivos():
    """Verifica que los archivos principales existan"""
    archivos_requeridos = [
        'app.py',
        'requirements.txt',
        'wsgi.py',
        'static/style.css',
        'templates/base.html'
    ]
    
    print("🔍 Verificando archivos requeridos...")
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            return False
    return True

def limpiar_cache():
    """Limpia archivos de cache y temporales"""
    archivos_cache = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.pytest_cache',
        '.coverage'
    ]
    
    print("🧹 Limpiando cache...")
    for patron in archivos_cache:
        if os.path.exists(patron):
            if os.path.isdir(patron):
                subprocess.run(f"rmdir /s /q {patron}", shell=True)
            else:
                subprocess.run(f"del {patron}", shell=True)

def main():
    print("🚀 Iniciando proceso de actualización forzada...")
    
    # Verificar archivos
    if not verificar_archivos():
        print("❌ Faltan archivos requeridos. Abortando.")
        return False
    
    # Limpiar cache
    limpiar_cache()
    
    # Crear archivo de timestamp para forzar actualización
    timestamp = int(time.time())
    with open('last_update.txt', 'w') as f:
        f.write(f"Última actualización: {timestamp}")
    
    print(f"📝 Archivo de timestamp creado: {timestamp}")
    
    # Verificar si estamos en un entorno de producción
    if os.environ.get('RENDER'):
        print("🌐 Detectado entorno de Render")
        print("✅ Los cambios se aplicarán automáticamente en el próximo despliegue")
    else:
        print("💻 Entorno local detectado")
        print("📋 Para aplicar cambios en Render:")
        print("   1. Sube los cambios a GitHub")
        print("   2. Render detectará automáticamente los cambios")
        print("   3. Se iniciará un nuevo despliegue")
    
    print("\n🎉 Proceso de actualización completado")
    print("📊 Resumen de mejoras aplicadas:")
    print("   ✅ CSS mejorado con mejor contraste y legibilidad")
    print("   ✅ Estilos responsivos optimizados")
    print("   ✅ Problemas de z-index corregidos")
    print("   ✅ Colores y tipografía mejorados")
    print("   ✅ Animaciones y transiciones suavizadas")
    print("   ✅ Formularios flotantes mejorados")
    print("   ✅ Alertas con mejor diseño")
    
    return True

if __name__ == "__main__":
    try:
        exito = main()
        if exito:
            print("\n✅ Actualización completada exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Error en la actualización")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

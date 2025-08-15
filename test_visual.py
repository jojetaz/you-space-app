#!/usr/bin/env python3
"""
Script para probar la aplicación localmente y verificar los cambios visuales
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError:
        print("❌ Flask no está instalado")
        return False
    
    try:
        import flask_sqlalchemy
        print(f"✅ Flask-SQLAlchemy {flask_sqlalchemy.__version__}")
    except ImportError:
        print("❌ Flask-SQLAlchemy no está instalado")
        return False
    
    try:
        import flask_login
        print(f"✅ Flask-Login instalado")
    except ImportError:
        print("❌ Flask-Login no está instalado")
        return False
    
    return True

def verificar_archivos_css():
    """Verifica que los archivos CSS estén presentes y sean válidos"""
    print("\n🎨 Verificando archivos CSS...")
    
    archivos_css = [
        'static/style.css',
        'static/css/style.css'
    ]
    
    for archivo in archivos_css:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                if '--primary-color' in contenido and '--card-bg' in contenido:
                    print(f"✅ {archivo} - Válido")
                else:
                    print(f"⚠️  {archivo} - Puede estar incompleto")
        else:
            print(f"❌ {archivo} - No encontrado")
    
    # Verificar imagen de fondo
    if os.path.exists('static/background.jpg'):
        print("✅ static/background.jpg - Encontrada")
    else:
        print("⚠️  static/background.jpg - No encontrada")

def iniciar_aplicacion():
    """Inicia la aplicación Flask localmente"""
    print("\n🚀 Iniciando aplicación Flask...")
    
    # Verificar que app.py existe
    if not os.path.exists('app.py'):
        print("❌ app.py no encontrado")
        return False
    
    try:
        # Iniciar la aplicación en segundo plano
        proceso = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un momento para que la aplicación se inicie
        time.sleep(3)
        
        # Verificar si el proceso sigue ejecutándose
        if proceso.poll() is None:
            print("✅ Aplicación iniciada correctamente")
            print("🌐 Abriendo navegador en http://localhost:5000")
            
            # Abrir navegador
            try:
                webbrowser.open('http://localhost:5000')
            except:
                print("⚠️  No se pudo abrir el navegador automáticamente")
            
            print("\n📋 Instrucciones:")
            print("   1. Revisa la aplicación en tu navegador")
            print("   2. Verifica que los estilos se vean correctamente")
            print("   3. Prueba la responsividad en diferentes tamaños")
            print("   4. Presiona Ctrl+C para detener la aplicación")
            
            try:
                proceso.wait()
            except KeyboardInterrupt:
                print("\n⏹️  Deteniendo aplicación...")
                proceso.terminate()
                proceso.wait()
                print("✅ Aplicación detenida")
            
            return True
        else:
            stdout, stderr = proceso.communicate()
            print(f"❌ Error al iniciar la aplicación:")
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_estructura():
    """Verifica la estructura del proyecto"""
    print("📁 Verificando estructura del proyecto...")
    
    directorios_requeridos = [
        'static',
        'static/css',
        'static/categorias',
        'static/uploads',
        'templates'
    ]
    
    for directorio in directorios_requeridos:
        if os.path.exists(directorio):
            print(f"✅ {directorio}/")
        else:
            print(f"❌ {directorio}/ - No encontrado")
    
    archivos_requeridos = [
        'app.py',
        'wsgi.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html'
    ]
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - No encontrado")

def main():
    print("🎨 Verificador de Cambios Visuales")
    print("=" * 40)
    
    # Verificar estructura
    verificar_estructura()
    
    # Verificar archivos CSS
    verificar_archivos_css()
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Faltan dependencias. Ejecuta: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todas las verificaciones completadas")
    
    # Preguntar si quiere iniciar la aplicación
    respuesta = input("\n¿Deseas iniciar la aplicación para probar los cambios? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        return iniciar_aplicacion()
    else:
        print("\n📋 Para probar manualmente:")
        print("   1. Ejecuta: python app.py")
        print("   2. Abre http://localhost:5000 en tu navegador")
        print("   3. Verifica que los estilos se vean correctamente")
        return True

if __name__ == "__main__":
    try:
        exito = main()
        if exito:
            print("\n✅ Verificación completada exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Error en la verificación")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

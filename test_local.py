#!/usr/bin/env python3
"""
Script para probar la aplicación localmente
"""

import os
import sys
from flask import Flask

# Configurar variables de entorno para pruebas
os.environ['FLASK_ENV'] = 'development'
os.environ['SECRET_KEY'] = 'test_secret_key'

def test_imports():
    """Probar que todas las importaciones funcionan"""
    try:
        from app import app, db
        print("✅ Importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_database():
    """Probar la base de datos"""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Base de datos creada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def test_templates():
    """Probar que las plantillas existen"""
    template_files = ['base.html', 'index.html', 'categoria.html', 'login.html']
    missing_files = []
    
    for template in template_files:
        if not os.path.exists(f'templates/{template}'):
            missing_files.append(template)
    
    if missing_files:
        print(f"❌ Plantillas faltantes: {missing_files}")
        return False
    else:
        print("✅ Todas las plantillas existen")
        return True

def test_static_files():
    """Probar que los archivos estáticos existen"""
    static_dirs = ['static', 'static/css', 'static/categorias']
    missing_dirs = []
    
    for static_dir in static_dirs:
        if not os.path.exists(static_dir):
            missing_dirs.append(static_dir)
    
    if missing_dirs:
        print(f"❌ Directorios estáticos faltantes: {missing_dirs}")
        return False
    else:
        print("✅ Directorios estáticos existen")
        return True

def main():
    """Función principal de pruebas"""
    print("🧪 PROBANDO APLICACIÓN LOCALMENTE")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_database,
        test_templates,
        test_static_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("✅ ¡Todas las pruebas pasaron! La aplicación está lista para desplegar.")
        return True
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores antes de desplegar.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
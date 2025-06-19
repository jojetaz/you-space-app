#!/usr/bin/env python3
"""
Script para forzar la actualización de la base de datos
"""

import sqlite3
import os

def forzar_actualizacion_db():
    """Fuerza la actualización de la base de datos"""
    
    db_path = 'ia_tools.db'
    
    if not os.path.exists(db_path):
        print("❌ No se encontró la base de datos")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Forzando actualización de la base de datos...")
        
        # Verificar y agregar columna imagen a categoria si no existe
        cursor.execute("PRAGMA table_info(categoria)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'imagen' not in columnas:
            print("➕ Agregando columna 'imagen' a tabla categoria...")
            cursor.execute("ALTER TABLE categoria ADD COLUMN imagen VARCHAR(200)")
            print("✅ Columna 'imagen' agregada a categoria")
        else:
            print("ℹ️  Columna 'imagen' ya existe en categoria")
        
        # Verificar y agregar columnas a herramienta
        cursor.execute("PRAGMA table_info(herramienta)")
        columnas_herramienta = [col[1] for col in cursor.fetchall()]
        
        if 'imagen' not in columnas_herramienta:
            print("➕ Agregando columna 'imagen' a tabla herramienta...")
            cursor.execute("ALTER TABLE herramienta ADD COLUMN imagen VARCHAR(200)")
            print("✅ Columna 'imagen' agregada a herramienta")
        else:
            print("ℹ️  Columna 'imagen' ya existe en herramienta")
        
        if 'video' not in columnas_herramienta:
            print("➕ Agregando columna 'video' a tabla herramienta...")
            cursor.execute("ALTER TABLE herramienta ADD COLUMN video VARCHAR(200)")
            print("✅ Columna 'video' agregada a herramienta")
        else:
            print("ℹ️  Columna 'video' ya existe en herramienta")
        
        # Verificar y agregar columna es_admin a usuario
        cursor.execute("PRAGMA table_info(usuario)")
        columnas_usuario = [col[1] for col in cursor.fetchall()]
        
        if 'es_admin' not in columnas_usuario:
            print("➕ Agregando columna 'es_admin' a tabla usuario...")
            cursor.execute("ALTER TABLE usuario ADD COLUMN es_admin BOOLEAN DEFAULT 0")
            print("✅ Columna 'es_admin' agregada a usuario")
        else:
            print("ℹ️  Columna 'es_admin' ya existe en usuario")
        
        # Actualizar registros existentes para asegurar compatibilidad
        print("🔄 Actualizando registros existentes...")
        
        # Asegurar que todas las categorías tengan el campo imagen
        cursor.execute("UPDATE categoria SET imagen = NULL WHERE imagen IS NULL")
        
        # Asegurar que todas las herramientas tengan los campos imagen y video
        cursor.execute("UPDATE herramienta SET imagen = NULL WHERE imagen IS NULL")
        cursor.execute("UPDATE herramienta SET video = NULL WHERE video IS NULL")
        
        # Asegurar que todos los usuarios tengan el campo es_admin
        cursor.execute("UPDATE usuario SET es_admin = 0 WHERE es_admin IS NULL")
        
        # Crear usuario administrador si no existe
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = 'admin@example.com'")
        if cursor.fetchone()[0] == 0:
            print("➕ Creando usuario administrador...")
            from werkzeug.security import generate_password_hash
            admin_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO usuario (email, password, nombre, es_admin)
                VALUES (?, ?, ?, ?)
            ''', ('admin@example.com', admin_password, 'Administrador', True))
            print("✅ Usuario administrador creado")
        
        # Crear categorías de ejemplo si no existen
        cursor.execute("SELECT COUNT(*) FROM categoria")
        if cursor.fetchone()[0] == 0:
            print("➕ Creando categorías de ejemplo...")
            categorias_ejemplo = [
                ('Generación de Video', 'Herramientas para crear y editar videos con IA'),
                ('Generación de Imágenes', 'Herramientas para crear imágenes con inteligencia artificial'),
                ('Generación de Música', 'Herramientas para crear música con IA'),
                ('Presentaciones', 'Herramientas para crear presentaciones automáticamente'),
                ('Edición de Video', 'Herramientas de edición de video asistida por IA'),
                ('Conversión de Formatos', 'Herramientas para convertir archivos entre formatos'),
                ('Automatización de Trabajos', 'Herramientas para automatizar tareas repetitivas'),
                ('Desarrollo Web', 'Herramientas para desarrollo web con IA'),
                ('Aplicaciones Móviles', 'Herramientas para desarrollo de apps móviles')
            ]
            
            for nombre, descripcion in categorias_ejemplo:
                cursor.execute('''
                    INSERT INTO categoria (nombre, descripcion, imagen)
                    VALUES (?, ?, ?)
                ''', (nombre, descripcion, None))
            print(f"✅ {len(categorias_ejemplo)} categorías de ejemplo creadas")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Base de datos actualizada exitosamente!")
        print("\n📋 Información de acceso:")
        print("   Email: admin@example.com")
        print("   Contraseña: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Forzando actualización de la base de datos...")
    forzar_actualizacion_db()
    print("\n✅ Proceso completado.") 
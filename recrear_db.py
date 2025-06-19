#!/usr/bin/env python3
"""
Script para recrear la base de datos con la estructura correcta
"""

import os
import sqlite3
from werkzeug.security import generate_password_hash

def recrear_base_datos():
    """Recrea la base de datos con la estructura correcta"""
    
    # Ruta de la base de datos
    db_path = 'ia_tools.db'
    
    # Eliminar la base de datos existente si existe
    if os.path.exists(db_path):
        print("🗑️  Eliminando base de datos existente...")
        os.remove(db_path)
        print("✅ Base de datos eliminada")
    
    try:
        # Crear nueva base de datos
        print("🔄 Creando nueva base de datos...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla usuario
        cursor.execute('''
            CREATE TABLE usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(120) UNIQUE NOT NULL,
                password VARCHAR(200) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                es_admin BOOLEAN DEFAULT 0
            )
        ''')
        print("✅ Tabla 'usuario' creada")
        
        # Crear tabla categoria
        cursor.execute('''
            CREATE TABLE categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                imagen VARCHAR(200)
            )
        ''')
        print("✅ Tabla 'categoria' creada con campo imagen")
        
        # Crear tabla herramienta
        cursor.execute('''
            CREATE TABLE herramienta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                url VARCHAR(200),
                imagen VARCHAR(200),
                video VARCHAR(200),
                categoria_id INTEGER NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categoria (id)
            )
        ''')
        print("✅ Tabla 'herramienta' creada")
        
        # Crear usuario administrador por defecto
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO usuario (email, password, nombre, es_admin)
            VALUES (?, ?, ?, ?)
        ''', ('admin@example.com', admin_password, 'Administrador', True))
        print("✅ Usuario administrador creado")
        
        # Crear algunas categorías de ejemplo
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
                INSERT INTO categoria (nombre, descripcion)
                VALUES (?, ?)
            ''', (nombre, descripcion))
        
        print(f"✅ {len(categorias_ejemplo)} categorías de ejemplo creadas")
        
        # Crear algunas herramientas de ejemplo
        herramientas_ejemplo = [
            (1, 'Runway ML', 'Plataforma de IA para creación de contenido visual y video', 'https://runwayml.com'),
            (1, 'Synthesia', 'Crear videos con avatares de IA', 'https://www.synthesia.io'),
            (2, 'Midjourney', 'Generador de imágenes con IA', 'https://www.midjourney.com'),
            (2, 'DALL-E', 'Generador de imágenes de OpenAI', 'https://openai.com/dall-e-2'),
            (3, 'Mubert', 'Generador de música con IA', 'https://mubert.com'),
            (3, 'Amper Music', 'Composición musical con inteligencia artificial', 'https://www.ampermusic.com'),
            (4, 'Beautiful.ai', 'Presentaciones automáticas con IA', 'https://www.beautiful.ai'),
            (4, 'Gamma', 'Crear presentaciones con IA', 'https://gamma.app'),
            (5, 'CapCut', 'Editor de video con efectos de IA', 'https://www.capcut.com'),
            (5, 'DaVinci Resolve', 'Editor profesional con herramientas de IA', 'https://www.blackmagicdesign.com/products/davinciresolve')
        ]
        
        for categoria_id, nombre, descripcion, url in herramientas_ejemplo:
            cursor.execute('''
                INSERT INTO herramienta (categoria_id, nombre, descripcion, url)
                VALUES (?, ?, ?, ?)
            ''', (categoria_id, nombre, descripcion, url))
        
        print(f"✅ {len(herramientas_ejemplo)} herramientas de ejemplo creadas")
        
        # Guardar cambios
        conn.commit()
        conn.close()
        
        print("\n🎉 Base de datos recreada exitosamente!")
        print("\n📋 Información de acceso:")
        print("   Email: admin@example.com")
        print("   Contraseña: admin123")
        print("\n🔗 Accede a la aplicación en: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al recrear la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Recreando base de datos...")
    recrear_base_datos()
    print("\n✅ Proceso completado.") 
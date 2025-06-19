#!/usr/bin/env python3
"""
Script para actualizar la base de datos y agregar el campo imagen a las categorías existentes
"""

import sqlite3
import os

def actualizar_base_datos():
    """Actualiza la base de datos para agregar el campo imagen a las categorías"""
    
    # Ruta de la base de datos
    db_path = 'ia_tools.db'
    
    if not os.path.exists(db_path):
        print("❌ No se encontró la base de datos. Ejecuta primero la aplicación.")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si el campo imagen ya existe en la tabla categoria
        cursor.execute("PRAGMA table_info(categoria)")
        columnas = [columna[1] for columna in cursor.fetchall()]
        
        if 'imagen' not in columnas:
            print("🔄 Agregando campo 'imagen' a la tabla categoria...")
            cursor.execute("ALTER TABLE categoria ADD COLUMN imagen VARCHAR(200)")
            conn.commit()
            print("✅ Campo 'imagen' agregado exitosamente a la tabla categoria")
        else:
            print("ℹ️  El campo 'imagen' ya existe en la tabla categoria")
        
        # Verificar la estructura de la tabla herramienta
        cursor.execute("PRAGMA table_info(herramienta)")
        columnas_herramienta = [columna[1] for columna in cursor.fetchall()]
        
        if 'imagen' not in columnas_herramienta:
            print("🔄 Agregando campo 'imagen' a la tabla herramienta...")
            cursor.execute("ALTER TABLE herramienta ADD COLUMN imagen VARCHAR(200)")
            conn.commit()
            print("✅ Campo 'imagen' agregado exitosamente a la tabla herramienta")
        else:
            print("ℹ️  El campo 'imagen' ya existe en la tabla herramienta")
        
        if 'video' not in columnas_herramienta:
            print("🔄 Agregando campo 'video' a la tabla herramienta...")
            cursor.execute("ALTER TABLE herramienta ADD COLUMN video VARCHAR(200)")
            conn.commit()
            print("✅ Campo 'video' agregado exitosamente a la tabla herramienta")
        else:
            print("ℹ️  El campo 'video' ya existe en la tabla herramienta")
        
        # Verificar la estructura de la tabla usuario
        cursor.execute("PRAGMA table_info(usuario)")
        columnas_usuario = [columna[1] for columna in cursor.fetchall()]
        
        if 'es_admin' not in columnas_usuario:
            print("🔄 Agregando campo 'es_admin' a la tabla usuario...")
            cursor.execute("ALTER TABLE usuario ADD COLUMN es_admin BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Campo 'es_admin' agregado exitosamente a la tabla usuario")
        else:
            print("ℹ️  El campo 'es_admin' ya existe en la tabla usuario")
        
        # Mostrar la estructura final de las tablas
        print("\n📋 Estructura actualizada de las tablas:")
        
        cursor.execute("PRAGMA table_info(categoria)")
        print("\nTabla 'categoria':")
        for columna in cursor.fetchall():
            print(f"  - {columna[1]} ({columna[2]})")
        
        cursor.execute("PRAGMA table_info(herramienta)")
        print("\nTabla 'herramienta':")
        for columna in cursor.fetchall():
            print(f"  - {columna[1]} ({columna[2]})")
        
        cursor.execute("PRAGMA table_info(usuario)")
        print("\nTabla 'usuario':")
        for columna in cursor.fetchall():
            print(f"  - {columna[1]} ({columna[2]})")
        
        conn.close()
        print("\n✅ Base de datos actualizada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Actualizando base de datos...")
    actualizar_base_datos()
    print("\n🎉 Proceso completado. Ahora puedes ejecutar la aplicación.") 
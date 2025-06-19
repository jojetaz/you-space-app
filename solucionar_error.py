#!/usr/bin/env python3
"""
Script para solucionar el error de sincronización entre SQLAlchemy y la base de datos
"""

import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def crear_app_temporal():
    """Crear una aplicación Flask temporal para acceder a SQLAlchemy"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ia_tools.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

def verificar_y_reparar_db():
    """Verificar y reparar la base de datos"""
    print("=== SOLUCIONANDO ERROR DE SINCRONIZACIÓN ===")
    
    # Crear aplicación temporal
    app = crear_app_temporal()
    db = SQLAlchemy(app)
    
    with app.app_context():
        try:
            # Verificar si la tabla existe
            result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categoria'")
            if not result.fetchone():
                print("❌ La tabla 'categoria' no existe")
                return False
            
            # Verificar estructura de la tabla
            result = db.engine.execute("PRAGMA table_info(categoria)")
            columns = result.fetchall()
            column_names = [col[1] for col in columns]
            
            print(f"Columnas encontradas: {column_names}")
            
            if 'imagen' not in column_names:
                print("❌ La columna 'imagen' no existe en la tabla categoria")
                print("Agregando columna 'imagen'...")
                
                # Agregar la columna imagen
                db.engine.execute("ALTER TABLE categoria ADD COLUMN imagen VARCHAR(200)")
                print("✅ Columna 'imagen' agregada exitosamente")
            else:
                print("✅ La columna 'imagen' ya existe")
            
            # Verificar que SQLAlchemy puede acceder a la tabla
            print("\nVerificando acceso de SQLAlchemy...")
            
            # Definir el modelo temporalmente
            class CategoriaTemp(db.Model):
                __tablename__ = 'categoria'
                id = db.Column(db.Integer, primary_key=True)
                nombre = db.Column(db.String(100), nullable=False)
                descripcion = db.Column(db.Text)
                imagen = db.Column(db.String(200), nullable=True)
            
            # Intentar hacer una consulta
            try:
                categorias = CategoriaTemp.query.all()
                print(f"✅ SQLAlchemy puede acceder a la tabla. Encontradas {len(categorias)} categorías")
                return True
            except Exception as e:
                print(f"❌ Error al consultar con SQLAlchemy: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error general: {e}")
            return False

def limpiar_cache_sqlalchemy():
    """Limpiar caché de SQLAlchemy"""
    print("\n=== LIMPIANDO CACHÉ DE SQLALCHEMY ===")
    
    # Eliminar archivos de caché de Python
    cache_dirs = ['__pycache__', 'venv/__pycache__']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            import shutil
            shutil.rmtree(cache_dir)
            print(f"✅ Eliminado directorio de caché: {cache_dir}")
    
    # Eliminar archivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
                print(f"✅ Eliminado archivo: {file}")

def recrear_base_datos():
    """Recrear la base de datos desde cero"""
    print("\n=== RECREANDO BASE DE DATOS ===")
    
    # Hacer backup de la base de datos actual
    if os.path.exists('ia_tools.db'):
        import shutil
        shutil.copy2('ia_tools.db', 'ia_tools_backup.db')
        print("✅ Backup creado: ia_tools_backup.db")
    
    # Eliminar la base de datos actual
    if os.path.exists('ia_tools.db'):
        os.remove('ia_tools.db')
        print("✅ Base de datos eliminada")
    
    # Crear nueva base de datos
    app = crear_app_temporal()
    db = SQLAlchemy(app)
    
    with app.app_context():
        # Definir modelos
        class Usuario(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password = db.Column(db.String(200), nullable=False)
            nombre = db.Column(db.String(100), nullable=False)
            es_admin = db.Column(db.Boolean, default=False)
        
        class Categoria(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(100), nullable=False)
            descripcion = db.Column(db.Text)
            imagen = db.Column(db.String(200), nullable=True)
            herramientas = db.relationship('Herramienta', backref='categoria', lazy=True)
        
        class Herramienta(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            nombre = db.Column(db.String(100), nullable=False)
            descripcion = db.Column(db.Text)
            url = db.Column(db.String(200))
            imagen = db.Column(db.String(200))
            video = db.Column(db.String(200))
            categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
            fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
        
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos recreada con estructura correcta")
        
        # Verificar estructura
        result = db.engine.execute("PRAGMA table_info(categoria)")
        columns = result.fetchall()
        print("Estructura de la tabla categoria:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

def main():
    """Función principal"""
    print("🔧 SOLUCIONADOR DE ERRORES DE BASE DE DATOS")
    print("=" * 50)
    
    # Opción 1: Intentar reparar
    print("\n1. Intentando reparar la base de datos actual...")
    if verificar_y_reparar_db():
        print("✅ Reparación exitosa")
        return
    
    # Opción 2: Limpiar caché
    print("\n2. Limpiando caché de SQLAlchemy...")
    limpiar_cache_sqlalchemy()
    
    # Opción 3: Recrear base de datos
    print("\n3. Recreando base de datos...")
    recrear_base_datos()
    
    print("\n✅ Proceso completado. Ahora puedes iniciar la aplicación.")

if __name__ == "__main__":
    main() 
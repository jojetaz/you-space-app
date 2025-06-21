#!/usr/bin/env python3
"""
Script para inicializar la base de datos en Render
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Crear aplicación Flask
app = Flask(__name__)

# Adaptar la URL de la base de datos para SQLAlchemy
database_url = os.environ.get('DATABASE_URL', 'sqlite:///ia_tools.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

def init_db():
    """Inicializar la base de datos"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        # Verificar si ya hay datos
        if Usuario.query.count() > 0:
            print("✅ La base de datos ya tiene datos")
            return
        
        # Crear usuario administrador
        admin = Usuario(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            nombre='Administrador',
            es_admin=True
        )
        db.session.add(admin)
        
        # Crear categorías de ejemplo
        categorias_ejemplo = [
            {
                'nombre': 'Chatbots',
                'descripcion': 'Herramientas para crear y gestionar chatbots inteligentes'
            },
            {
                'nombre': 'Generación de Imágenes',
                'descripcion': 'IA para crear y editar imágenes de alta calidad'
            },
            {
                'nombre': 'Análisis de Texto',
                'descripcion': 'Herramientas para procesamiento y análisis de texto'
            }
        ]
        
        for cat_data in categorias_ejemplo:
            categoria = Categoria(**cat_data)
            db.session.add(categoria)
        
        db.session.commit()
        print("✅ Datos iniciales agregados exitosamente")

if __name__ == "__main__":
    init_db() 
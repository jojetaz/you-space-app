#!/usr/bin/env python3
"""
Archivo WSGI para servir la aplicación Flask en producción
"""

from app import app

if __name__ == "__main__":
    app.run() 
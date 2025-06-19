#!/usr/bin/env python3
"""
Archivo WSGI para servir la aplicación Flask en producción
Configurado para trabajar con Cloudflare y dominio you-space.info
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Importar la aplicación Flask
from app import app

# Configuración para producción
if __name__ == "__main__":
    # Configuración para desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=False)
else:
    # Configuración para producción
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'you-space.info' 
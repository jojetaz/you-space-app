"""
Archivo de configuración WSGI para PythonAnywhere
"""
import os
import sys

# Agregar el directorio de la aplicación al path
path = '/home/USUARIO/you-space-app'
if path not in sys.path:
    sys.path.append(path)

# Importar la aplicación Flask
from app import app as application

# Configuración para producción
application.config['PREFERRED_URL_SCHEME'] = 'https' 
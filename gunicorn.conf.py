#!/usr/bin/env python3
"""
Configuración de Gunicorn para producción
Optimizado para trabajar con Cloudflare y dominio you-space.info
"""

import multiprocessing
import os

# Configuración del servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de SSL (si es necesario)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Configuración de proxy
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Configuración de preload
preload_app = True

def when_ready(server):
    """Función que se ejecuta cuando el servidor está listo"""
    server.log.info("Servidor Gunicorn listo para recibir conexiones")

def worker_int(worker):
    """Función que se ejecuta cuando un worker se reinicia"""
    worker.log.info("Worker reiniciado")

def pre_fork(server, worker):
    """Función que se ejecuta antes de crear workers"""
    server.log.info("Creando worker")

def post_fork(server, worker):
    """Función que se ejecuta después de crear workers"""
    server.log.info("Worker creado") 
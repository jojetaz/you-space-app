# Portafolio de Herramientas IA

Este es un portafolio web que organiza y muestra diferentes herramientas de Inteligencia Artificial categorizadas por tipo de uso.

## Características

- Categorización de herramientas de IA
- Sistema de autenticación de usuarios
- Panel de administración
- Carga de imágenes y videos
- Interfaz moderna y responsiva
- Gestión de categorías y herramientas

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd portafolio-ia
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

5. Inicializar la base de datos:
```bash
python init_db.py
```

## Uso

1. Iniciar el servidor:
```bash
python app.py
```

2. Abrir el navegador y acceder a:
```
http://localhost:5000
```

3. Credenciales de administrador:
- Email: admin@example.com
- Contraseña: admin123

## Estructura del Proyecto

```
portafolio-ia/
├── app.py              # Aplicación principal
├── init_db.py          # Script de inicialización de la base de datos
├── requirements.txt    # Dependencias del proyecto
├── static/            # Archivos estáticos
│   ├── css/
│   └── uploads/       # Carpeta para archivos subidos
└── templates/         # Plantillas HTML
    ├── base.html
    ├── index.html
    ├── categoria.html
    └── login.html
```

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 
# You Space - Herramientas de IA

Una aplicación web para gestionar y organizar herramientas de Inteligencia Artificial.

## 🚀 Despliegue en Render

### Configuración Automática

La aplicación está configurada para desplegarse automáticamente en Render. Los archivos de configuración incluyen:

- `render.yaml` - Configuración del servicio web
- `requirements.txt` - Dependencias de Python
- `wsgi.py` - Punto de entrada para Gunicorn
- `init_db.py` - Inicialización de la base de datos

### Pasos para Desplegar

1. **Conectar con GitHub**:
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - Haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub

2. **Configuración del Servicio**:
   - **Name**: `you-space-app` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python init_db.py`
   - **Start Command**: `gunicorn wsgi:app`

3. **Variables de Entorno** (se configuran automáticamente):
   - `PYTHON_VERSION`: `3.9.16`
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generado automáticamente
   - `DATABASE_URL`: `sqlite:///ia_tools.db`

4. **Desplegar**:
   - Haz clic en "Create Web Service"
   - Render construirá y desplegará automáticamente tu aplicación

### Credenciales por Defecto

- **Email**: `admin@example.com`
- **Contraseña**: `admin123`

## 🛠️ Desarrollo Local

### Requisitos

- Python 3.9+
- pip

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <tu-repositorio>
   cd "base de datos ia"
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar base de datos**:
   ```bash
   python init_db.py
   ```

5. **Ejecutar aplicación**:
   ```bash
   python app.py
   ```

6. **Probar localmente**:
   ```bash
   python test_local.py
   ```

### Estructura del Proyecto

```
├── app.py                 # Aplicación principal Flask
├── wsgi.py               # Configuración WSGI para producción
├── init_db.py            # Inicialización de base de datos
├── requirements.txt      # Dependencias de Python
├── render.yaml           # Configuración de Render
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── categoria.html
│   └── login.html
├── static/               # Archivos estáticos
│   ├── css/
│   ├── categorias/
│   └── uploads/
└── tema/                 # Tema original (copia de seguridad)
```

## 🔧 Solución de Problemas

### Error de Build en Render

Si encuentras el error "Salió con el estado 1 mientras creaba su código":

1. **Verificar dependencias**: Asegúrate de que `requirements.txt` esté actualizado
2. **Probar localmente**: Ejecuta `python test_local.py` antes de desplegar
3. **Revisar logs**: En Render Dashboard, ve a "Logs" para ver errores específicos

### Problemas Comunes

- **Importación de módulos**: Las importaciones están configuradas para funcionar en Render
- **Base de datos**: Se inicializa automáticamente durante el build
- **Archivos estáticos**: Se sirven desde la carpeta `static/`

## 📝 Características

- ✅ Gestión de categorías de herramientas de IA
- ✅ Subida y gestión de imágenes
- ✅ Sistema de autenticación
- ✅ Interfaz responsive
- ✅ Base de datos SQLite
- ✅ Despliegue automático en Render

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 
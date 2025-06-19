from app import app, db, Usuario, Categoria
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()

        # Crear usuario administrador solo si no existe
        admin_email = 'admin@example.com'
        admin = Usuario.query.filter_by(email=admin_email).first()
        if not admin:
            admin = Usuario(
                email=admin_email,
                password=generate_password_hash('admin123'),
                nombre='Administrador',
                es_admin=True
            )
            db.session.add(admin)

        # Crear categorías predefinidas solo si no existen
        categorias = [
            {'nombre': 'Generación de Video', 'descripcion': 'Herramientas para crear y editar videos usando IA'},
            {'nombre': 'Generación de Música', 'descripcion': 'Herramientas para crear y modificar música con IA'},
            {'nombre': 'Generación de Imágenes', 'descripcion': 'Herramientas para crear y editar imágenes usando IA'},
            {'nombre': 'Presentaciones', 'descripcion': 'Herramientas para crear presentaciones con IA'},
            {'nombre': 'Edición de Video', 'descripcion': 'Herramientas de IA para editar y mejorar videos'},
            {'nombre': 'Conversión de Formatos', 'descripcion': 'Herramientas para convertir entre diferentes formatos usando IA'},
            {'nombre': 'Automatización de Trabajos', 'descripcion': 'Herramientas para automatizar tareas con IA'},
            {'nombre': 'Desarrollo Web', 'descripcion': 'Herramientas de IA para desarrollo web'},
            {'nombre': 'Aplicaciones Móviles', 'descripcion': 'Herramientas de IA para desarrollo de apps móviles'}
        ]
        for cat in categorias:
            existe = Categoria.query.filter_by(nombre=cat['nombre']).first()
            if not existe:
                db.session.add(Categoria(**cat))

        # Guardar cambios
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada con éxito!") 
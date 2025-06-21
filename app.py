from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')

# Adaptar la URL de la base de datos para SQLAlchemy
database_url = os.environ.get('DATABASE_URL', 'sqlite:///ia_tools.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Asegurar que exista el directorio de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Imágenes predeterminadas (definidas localmente para evitar problemas de importación)
CATEGORIA_IMAGES = {
    'Generación de Video': 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&auto=format&fit=crop',
    'Generación de Música': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop',
    'Generación de Imágenes': 'https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800&auto=format&fit=crop',
    'Generación de Texto': 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&auto=format&fit=crop',
    'Generación de Código': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop',
    'default': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&auto=format&fit=crop'
}

HERRAMIENTA_IMAGES = {
    'ChatGPT': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&auto=format&fit=crop',
    'DALL-E': 'https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800&auto=format&fit=crop',
    'Midjourney': 'https://images.unsplash.com/photo-1682687220063-4742bd7fd538?w=800&auto=format&fit=crop',
    'Stable Diffusion': 'https://images.unsplash.com/photo-1682687220063-4742bd7fd538?w=800&auto=format&fit=crop',
    'GitHub Copilot': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop',
    'default': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&auto=format&fit=crop'
}

# Funciones de ayuda para las imágenes
def get_categoria_imagen(nombre):
    import os
    from flask import url_for
    nombre_archivo_base = nombre.lower().replace(' ', '_')
    extensiones = ['.jpg', '.jpeg', '.png']
    for ext in extensiones:
        nombre_archivo = nombre_archivo_base + ext
        ruta_local = os.path.join(app.static_folder, 'categorias', nombre_archivo)
        if os.path.exists(ruta_local):
            return url_for('static', filename=f'categorias/{nombre_archivo}')
    return CATEGORIA_IMAGES.get(nombre, CATEGORIA_IMAGES['default'])

def get_herramienta_imagen(nombre):
    return HERRAMIENTA_IMAGES.get(nombre, HERRAMIENTA_IMAGES['default'])

# Agregar las funciones al contexto de las plantillas
@app.context_processor
def utility_processor():
    return {
        'categoria_imagen': get_categoria_imagen,
        'herramienta_imagen': get_herramienta_imagen
    }

# Modelos de la base de datos
class Usuario(UserMixin, db.Model):
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
    
    def __init__(self, **kwargs):
        super(Categoria, self).__init__(**kwargs)
        # Asegurar que imagen tenga un valor por defecto
        if not hasattr(self, 'imagen') or self.imagen is None:
            self.imagen = None

class Herramienta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    url = db.Column(db.String(200))
    imagen = db.Column(db.String(200))
    video = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas principales
@app.route('/')
def index():
    categorias = Categoria.query.all()
    return render_template('index.html', categorias=categorias)

@app.route('/categoria/<int:id>')
def categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return render_template('categoria.html', categoria=categoria)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciales inválidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    # Obtener el ID de la categoría si existe (para edición)
    categoria_id = request.form.get('categoria_id')
    
    if categoria_id:
        # Modo edición
        categoria = Categoria.query.get_or_404(categoria_id)
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form['descripcion']
    else:
        # Modo creación
        categoria = Categoria(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion']
        )
        db.session.add(categoria)
    
    # Manejar la imagen si se proporciona una
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            # Asegurar que el directorio de uploads existe
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # Guardar la imagen
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            categoria.imagen = filename
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar_categoria/<int:categoria_id>', methods=['POST'])
def eliminar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    
    # Eliminar todas las herramientas asociadas
    for herramienta in categoria.herramientas:
        # Eliminar la imagen de la herramienta si existe
        if herramienta.imagen:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], herramienta.imagen))
            except:
                pass
        db.session.delete(herramienta)
    
    # Eliminar la imagen de la categoría si existe
    if categoria.imagen:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], categoria.imagen))
        except:
            pass
    
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/agregar_herramienta/<int:categoria_id>', methods=['POST'])
def agregar_herramienta(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    
    # Obtener el ID de la herramienta si existe (para edición)
    herramienta_id = request.form.get('herramienta_id')
    
    if herramienta_id:
        # Modo edición
        herramienta = Herramienta.query.get_or_404(herramienta_id)
        herramienta.nombre = request.form['nombre']
        herramienta.descripcion = request.form['descripcion']
        herramienta.url = request.form['url']
        herramienta.video = request.form.get('video', '')
    else:
        # Modo creación
        herramienta = Herramienta(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            url=request.form['url'],
            video=request.form.get('video', ''),
            categoria_id=categoria_id
        )
        db.session.add(herramienta)
    
    # Manejar la imagen si se proporciona una
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            # Guardar la imagen
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)
            herramienta.imagen = filename
    
    db.session.commit()
    return redirect(url_for('categoria', id=categoria_id))

@app.route('/eliminar_herramienta/<int:herramienta_id>', methods=['POST'])
def eliminar_herramienta(herramienta_id):
    herramienta = Herramienta.query.get_or_404(herramienta_id)
    categoria_id = herramienta.categoria_id
    
    # Eliminar la imagen si existe
    if herramienta.imagen:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], herramienta.imagen))
        except:
            pass
    
    db.session.delete(herramienta)
    db.session.commit()
    flash('Herramienta eliminada exitosamente', 'success')
    return redirect(url_for('categoria', id=categoria_id))

if __name__ == '__main__':
    with app.app_context():
        # Solo crear las tablas si no existen
        if not os.path.exists('ia_tools.db'):
            print("Creando base de datos inicial...")
            db.create_all()
        else:
            print("Base de datos existente encontrada, saltando creación...")
    app.run(debug=True) 
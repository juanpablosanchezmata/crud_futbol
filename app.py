import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Importar db desde extensions.py
from extensions import db 
from models import Team # Importar el modelo aquí, DESPUÉS de importar db

# Carga .env para desarrollo local
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key")

# DATABASE_URL debe estar en variables de entorno: ejemplo:
# postgres://user:pass@host:port/dbname (Render proporciona DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Define la variable de entorno DATABASE_URL apuntando a PostgreSQL")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db aquí (patrón de aplicación y contexto)
db.init_app(app)

# Crea tablas si no existen (útil para deploy rápido; para producción usa migrations)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    equipos = Team.query.order_by(Team.id).all()
    return render_template('index.html', equipos=equipos)

# Create - formulario
@app.route('/equipos/new', methods=['GET', 'POST'])
def create_equipo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ciudad = request.form.get('ciudad')
        estadio = request.form.get('estadio')
        entrenador = request.form.get('entrenador')
        equipo = Team(nombre=nombre, ciudad=ciudad, estadio=estadio, entrenador=entrenador)
        db.session.add(equipo)
        db.session.commit()
        flash(f'Equipo "{nombre}" creado correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

# Read - ver detalle
@app.route('/equipos/<int:id>')
def show_equipo(id):
    equipo = Team.query.get_or_404(id)
    return render_template('show.html', equipo=equipo)

# Update - editar
@app.route('/equipos/<int:id>/edit', methods=['GET', 'POST'])
def edit_equipo(id):
    equipo = Team.query.get_or_404(id)
    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.ciudad = request.form.get('ciudad')
        equipo.estadio = request.form.get('estadio')
        equipo.entrenador = request.form.get('entrenador')
        db.session.commit()
        flash(f'Equipo "{equipo.nombre}" actualizado.', 'success')
        
        # 🔑 CAMBIO CLAVE: Redirige al índice después de editar
        return redirect(url_for('index'))
        
    return render_template('edit.html', equipo=equipo)

# Delete
@app.route('/equipos/<int:id>/delete', methods=['POST'])
def delete_equipo(id):
    equipo = Team.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash(f'Equipo "{equipo.nombre}" eliminado.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # puerto para desarrollo
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
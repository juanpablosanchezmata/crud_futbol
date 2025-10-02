from flask_sqlalchemy import SQLAlchemy
from app import db  # cuidado con imports circulares; alternativa: inicializar db aquí

# Si prefieres separar, haz db = SQLAlchemy() en models y en app hacer db.init_app(app).
# Para simplicidad usamos el db importado del app principal.

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(120))
    estadio = db.Column(db.String(120))
    entrenador = db.Column(db.String(120))

    def __repr__(self):
        return f'<Team {self.nombre}>'

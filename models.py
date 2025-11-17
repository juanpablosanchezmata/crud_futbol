# models.py (Corregido)

# **Cambio clave: Importar db desde extensions.py**
from extensions import db 

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(120))
    estadio = db.Column(db.String(120))
    entrenador = db.Column(db.String(120))

    def __repr__(self):
        return f'<Team {self.nombre}>'
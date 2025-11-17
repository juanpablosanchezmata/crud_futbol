# extensions.py

from flask_sqlalchemy import SQLAlchemy

# Se crea la instancia de SQLAlchemy sin pasarle la aplicación (lazy initialization)
db = SQLAlchemy()
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# -----------------------
# USUARIOS DEL SISTEMA
# -----------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, usuario1, usuario2, usuario3


# -----------------------
# PACIENTE
# -----------------------
class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    eliminado = db.Column(db.Boolean, default=False)

    historia_clinica = db.relationship(
        'HistoriaClinica',
        backref='paciente',
        uselist=False,
        cascade='all, delete-orphan'
    )


# -----------------------
# HISTORIA CLÍNICA (1:1)
# -----------------------
class HistoriaClinica(db.Model):
    __tablename__ = 'historias_clinicas'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey('pacientes.id'),
        nullable=False,
        unique=True
    )

    diagnostico = db.Column(db.Text, nullable=False)
    observaciones = db.Column(db.Text)

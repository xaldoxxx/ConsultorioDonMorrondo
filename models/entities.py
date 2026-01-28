
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Paciente(db.Model):
    __tablename__ = 'paciente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    eliminado = db.Column(db.Boolean, default=False)

    historia = db.relationship(
        'HistoriaClinica',
        backref='paciente',
        uselist=False
    )

class HistoriaClinica(db.Model):
    __tablename__ = 'historia_clinica'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey('paciente.id'),
        unique=True,
        nullable=False
    )
    grupo_sanguineo = db.Column(db.String(5))
    eliminado = db.Column(db.Boolean, default=False)

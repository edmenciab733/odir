from extensions.database import db


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __repr__(self):
        return f"Parameter model: {self.empresa}, created at {self.date_created}"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(600), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


class PredictML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(300), nullable=False, unique=True)
    diagnostico = db.Column(db.String(300), nullable=False)
    codigo_externo = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())








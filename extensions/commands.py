import hashlib
from .database import db
from models.model import Empresa, PredictML, User

def create_db():
    """Creates database"""
    #db.crea\te_all()

def drop_db():
    """Drop / Clean database - DANGER ACTION"""
    db.drop_all()

def create_model_table():
    """Create table model in the database"""
    Empresa.__table__.create(db.engine, checkfirst=True)
    User.__table__.create(db.engine, checkfirst=True)
    PredictML.__table__.create(db.engine, checkfirst=True)
    u = User.query.filter(User.email == 'admin.py@odir.ia' , User.active == True).first()
    if u is None:
        e = Empresa()
        e.empresa = "Cavallaro"
        db.session.add(e)
        db.session.commit()  
        u = User()
        u.email = 'admin.py@odir.ia'
        u.name = 'root'
        u.active = True
        u.empresa_id = e.id
        u.password = hashlib.md5("123$123$cava$ia".encode("utf-8")).hexdigest()
        db.session.add(u)
        db.session.commit()  



def init_app(app):
    # add multiple commands in a bulk
    with app.app_context():
        #create_db()
        create_model_table()

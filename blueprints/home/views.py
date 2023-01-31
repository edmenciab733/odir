import os
from flask import Blueprint, redirect, render_template, request, send_from_directory, session
from PIL import Image
from  ml.inferencia import Inferencia
from models.model import PredictML
import json
from extensions.database import db
adivinar = Inferencia()

home = Blueprint('home', __name__, template_folder="templates", static_folder='static', static_url_path='/home/static')

@home.before_request
def verify_session():
    if session.get("usuario") == None:
        return redirect("/login") 
    else:
        print(session["usuario"])


@home.route("/")
def index():
    return render_template("home.html")

@home.route("/inferencia", methods=[ 'POST'])
def inferencia():
     if request.method == 'POST':
        image   = request.files['file']
        image, path, externo = adivinar.request_file_to_image(image)
        cataratas, diabetes, glaucoma, miopia = adivinar.diagnostico(image)
        p = PredictML()
        p.path = path
        p.codigo_externo = externo
        p.diagnostico = json.dumps(dict( Cataratas = "{:.3f}".format(cataratas), Diabetes = "{:.3f}".format(diabetes), Glaucoma = "{:.3f}".format(glaucoma), Miopia = "{:.3f}".format(miopia)))
        db.session.add(p)
        db.session.commit()
        return p.diagnostico


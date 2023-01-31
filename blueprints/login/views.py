import os
from flask import Blueprint, redirect, render_template, request, send_from_directory, session
import hashlib

from models.model import User

login = Blueprint('login', __name__, template_folder="templates", static_folder='static', static_url_path='/login/static')




def md5_decryptor(usuario, password):
    u = User.query.filter(User.email == usuario , User.active == True).first()
    if u is None:
        return False
    elif u.password == hashlib.md5(password.encode("utf-8")).hexdigest():
        session['usuario'] = u
        return True
    else:
        return False
    

@login.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(login.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login.route("/login",  methods=[ 'GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if md5_decryptor(email, password):
            return redirect("/")
        else:
            return render_template("login.html")
    else:
        
        return render_template("login.html")


@login.route("/logout",  methods=[ 'GET','POST'])
def logout():
    if not session['usuario'] is None:
        session['usuario'] = None
    return redirect("/login")
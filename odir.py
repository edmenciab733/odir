import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


from flask import Flask
from flask_session import Session
from extensions import database, commands
from blueprints.login.views import login
from blueprints.home.views import home

def create_flask():
    tocadorcia = Flask(__name__, static_folder='static', template_folder='custom_html' )
    tocadorcia.config["SESSION_PERMANENT"] = False
    tocadorcia.config["SESSION_TYPE"] = "filesystem"
    tocadorcia.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    tocadorcia.config['MAX_CONTENT_LENGTH'] = 92 * 1000 * 1000

    Session(tocadorcia)    
    # setup with the configuration provided by the user / environment
    tocadorcia.config.from_object('config.DevelopmentConfig')

    # setup all our dependencies
    database.init_app(tocadorcia)
    commands.init_app(tocadorcia)

    tocadorcia.register_blueprint(login)
    tocadorcia.register_blueprint(home)

    return tocadorcia

if __name__ == "odir":
    app = create_flask()
    app.run()
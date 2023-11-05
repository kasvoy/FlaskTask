from flask import Flask
from . import auth, tasks

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = '3c8b10ab0b565271a32d5289b76a478b'

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(tasks.tasks_bp)
    
    return app
from flask import Flask
from . import auth, tasks



def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = '3c8b10ab0b565271a32d5289b76a478b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(tasks.tasks_bp)

    from .models import User, Task, db, login_manager

    db.init_app(app)  
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        db.create_all()

    return app


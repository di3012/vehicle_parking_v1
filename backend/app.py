from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from flask_session import Session

from config import devConfig
from models import db, User, Role
from routes.login_register import login_register
from routes.admin import admin_routes
from routes.user import user_routes

from celery_redis import celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(devConfig)

    celery.conf.update(app.config)

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False
    Session(app)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Register routes
    app.register_blueprint(login_register)
    app.register_blueprint(admin_routes)
    app.register_blueprint(user_routes)

    return app

# ✅ Only run the server when called directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="localhost")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    from app.routes import posts_bp
    app.register_blueprint(posts_bp)

    # with app.app_context():
    #     db.create_all()

    return app

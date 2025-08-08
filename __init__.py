from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    from login import login_blueprint
    from routes import recipe_blueprint

    app.register_blueprint(login_blueprint, url_prefix="/auth")
    app.register_blueprint(recipe_blueprint, url_prefix="/recipes")

    return app

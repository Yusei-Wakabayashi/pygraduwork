from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

db = SQLAlchemy()

def create_app():
    # appの設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    # DBの設定
    db.init_app(app)
    Migrate(app, db)
    # Seederの設定
    FlaskSeeder(app, db)
    
    # Blueprintの登録
    from flask_app.controllers.index import index_bp
    app.register_blueprint(index_bp)

    return app
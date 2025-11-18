from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # REGISTER ROUTES
    from app.routes.jabatan_routes import jabatan_bp
    from app.routes.status_kerja_routes import status_kerja_bp
    from app.routes.karyawan_routes import karyawan_bp
    from app.routes.status_pernikahan_routes import status_pernikahan_bp

    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(status_kerja_bp, url_prefix='/api/status-kerja')
    app.register_blueprint(karyawan_bp, url_prefix='/api/karyawan')
    app.register_blueprint(status_pernikahan_bp, url_prefix='/api/status-pernikahan')

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

from app.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # REGISTER ROUTES
    from app.routes import (
        jabatan_bp, 
        status_kerja_bp, 
        karyawan_bp, 
        status_pernikahan_bp,
        kondisi_akun_bp,
        agama_bp,
        gaji_rule_bp
    )
    
    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(status_kerja_bp, url_prefix='/api/status-kerja')
    app.register_blueprint(karyawan_bp, url_prefix='/api/karyawan')
    app.register_blueprint(status_pernikahan_bp, url_prefix='/api/status-pernikahan')
    app.register_blueprint(kondisi_akun_bp, url_prefix='/api/kondisi-akun')
    app.register_blueprint(agama_bp, url_prefix='/api/agama')
    app.register_blueprint(gaji_rule_bp, url_prefix='/api/gaji-rule')


    return app

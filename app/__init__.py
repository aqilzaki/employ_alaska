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
        gaji_rule_bp,
        departemen_bp,
        gaji_setting_bp
    )
    
    from app.routes.mssql_routes.mssql_routes import mssql_bp
    # route for MSSQL 
    app.register_blueprint(mssql_bp, url_prefix='/api/mssql')

    # routes for MYSQL managed models
    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(status_kerja_bp, url_prefix='/api/status-kerja')
    app.register_blueprint(karyawan_bp, url_prefix='/api/karyawan')
    app.register_blueprint(status_pernikahan_bp, url_prefix='/api/status-pernikahan')
    app.register_blueprint(kondisi_akun_bp, url_prefix='/api/kondisi-akun')
    app.register_blueprint(agama_bp, url_prefix='/api/agama')
    app.register_blueprint(gaji_rule_bp, url_prefix='/api/gaji-rule')
    app.register_blueprint(departemen_bp, url_prefix='/api/departemen')
    app.register_blueprint(gaji_setting_bp, url_prefix='/api/gaji-setting')

    return app

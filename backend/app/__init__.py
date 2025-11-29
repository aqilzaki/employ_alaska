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

    with app.app_context():
        from app.models.jabatan import Jabatan
        from app.models.karyawan import Karyawan
        from app.models.status_kerja import StatusKerja
        from app.models.status_pernikahan import StatusPernikahan
        from app.models.kondisi_akun import kondisiAkun
        from app.models.agama import Agama

    # REGISTER ROUTES
    from app.routes.jabatan_routes import jabatan_bp
    from app.routes.status_kerja_routes import status_kerja_bp
    from app.routes.karyawan_routes import karyawan_bp
    from app.routes.status_pernikahan_routes import status_pernikahan_bp
    from app.routes.kondisi_akun_routes import kondisi_akun_bp

    app.register_blueprint(jabatan_bp, url_prefix='/api/jabatan')
    app.register_blueprint(status_kerja_bp, url_prefix='/api/status-kerja')
    app.register_blueprint(karyawan_bp, url_prefix='/api/karyawan')
    app.register_blueprint(status_pernikahan_bp, url_prefix='/api/status-pernikahan')
    app.register_blueprint(kondisi_akun_bp, url_prefix='/api/kondisi-akun')

    return app

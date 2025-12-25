from app.routes.jabatan_routes import jabatan_bp
from app.routes.status_kerja_routes import status_kerja_bp
from app.routes.karyawan_routes import karyawan_bp
from app.routes.status_pernikahan_routes import status_pernikahan_bp
from app.routes.kondisi_akun_routes import kondisi_akun_bp
from app.routes.agama_routes import agama_bp
from app.routes.gaji_rule_routes import gaji_rule_bp
from app.routes.departemen_routes import departemen_bp
from app.routes.gaji_setting_routes import gaji_setting_bp
from app.routes.absensi_operator_routes import absensi_operator_bp ,absensi_ae_bp
from app.routes.kunjungan_routes import kunjungan_bp
from app.routes.report_absensi_routes import report_absensi_bp
__all__ = [
           'jabatan_bp', 
           'status_kerja_bp',
           'gaji_rule_bp' ,
           'karyawan_bp', 
           'status_pernikahan_bp', 
           'kondisi_akun_bp', 
           'agama_bp', 
           'departemen_bp',
           'gaji_setting_bp', 
           'absensi_operator_bp',
           'kunjungan_bp',
           'absensi_ae_bp',
              'report_absensi_bp'
           ]
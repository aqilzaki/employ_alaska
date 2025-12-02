from app import db

class Jabatan(db.Model):
    __tablename__ = 'jabatan_karyawan'
    
    id = db.Column(db.String(255), primary_key=True)
    nama_jabatan = db.Column(db.String(255), nullable=False)
    
    # Relationship
    gaji_rules = db.relationship('GajiRule', back_populates='jabatan', lazy=True)
    karyawan = db.relationship('Karyawan', back_populates='jabatan', lazy=True)
    gaji_setting = db.relationship('GajiSetting', back_populates='jabatan', lazy=True)
    
    def __repr__(self):
        return f'<Jabatan {self.nama_jabatan}>'
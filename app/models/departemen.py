from app import db

class Departemen(db.Model):
    __tablename__ = 'departemen'
    
    id = db.Column(db.String(255), primary_key=True)
    nama_departemen = db.Column(db.String(255), nullable=False)
    
    # Relationships
    karyawan = db.relationship('Karyawan', back_populates='departemen', lazy=True)  
    gaji_setting = db.relationship('GajiSetting', back_populates='departemen', lazy=True)
    
    def __repr__(self):
        return f'<Departemen {self.nama_departemen}>'
    
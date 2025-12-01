from app import db

class kondisiAkun(db.Model):
    __tablename__ = 'kondisi_akun'
    
    id = db.Column(db.String(255), primary_key=True)
    nama_kondisi_akun = db.Column(db.String(255), nullable=False)
    
    # Relationship
    karyawan = db.relationship('Karyawan', back_populates='kondisi_akun', lazy=True)
    
    def __repr__(self):
        return f'<kondisiAkun {self.kondisi_Akun}>'
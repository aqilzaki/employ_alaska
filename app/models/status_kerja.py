from app import db

class StatusKerja(db.Model):
    __tablename__ = 'status_kerja_karyawan'
    
    id = db.Column(db.String(255), primary_key=True)
    nama_status = db.Column(db.String(255), nullable=False)
    
    # Relationship
    karyawan = db.relationship('Karyawan', back_populates='status_kerja', lazy=True)
    
    def __repr__(self):
        return f'<StatusKerja {self.nama_status}>'
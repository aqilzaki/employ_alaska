from app import db

class Agama(db.Model):
    __tablename__ = 'agama'
    
    id = db.Column(db.String(255), primary_key=True)
    nama_agama = db.Column(db.String(255), nullable=False)
    
    # Relationship
    karyawan = db.relationship('Karyawan', back_populates='agama', lazy=True)
    
    def __repr__(self):
        return f'<Agama {self.agama}>'
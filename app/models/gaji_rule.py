from app import db

class GajiRule(db.Model):
    __tablename__ = 'gaji_rule'
    
    id = db.Column(db.String(255), primary_key=True)
    id_jabatan_karyawan = db.Column(db.String(255), db.ForeignKey('jabatan_karyawan.id'), nullable=False)
    formula = db.Column(db.Text, nullable=False)
    variables = db.Column(db.JSON, nullable=True)

    # Relationship
    jabatan = db.relationship('Jabatan', back_populates='gaji_rules', lazy=True)
    
    def __repr__(self):
        return f'<GajiRule {self.nama_rule}>'
    

from app import db

class GajiSetting(db.Model):
    __tablename__ = 'gaji_setting'

    id = db.Column(db.String(255), primary_key=True)

    departemen_id = db.Column(db.String(255), db.ForeignKey('departemen.id'), nullable=False)
    jabatan_id = db.Column(db.String(255), db.ForeignKey('jabatan_karyawan.id'), nullable=False)
    status_kerja_id = db.Column(db.String(255), db.ForeignKey('status_kerja_karyawan.id'), nullable=False)

    gaji_pokok = db.Column(db.Integer, nullable=False)
    tunjangan_pokok = db.Column(db.Integer, nullable=False)

    total_tunjangan_opsional = db.Column(db.Integer, default=0)
    total_potongan_opsional = db.Column(db.Integer, default=0)
    total_gaji = db.Column(db.Integer, default=0)

    # Relationship
    jabatan = db.relationship('Jabatan', back_populates='gaji_setting')
    status_kerja = db.relationship('StatusKerja', back_populates='gaji_setting')
    tunjangan_opsional = db.relationship('GajiSettingTunjangan', back_populates='gaji_setting', cascade="all, delete")
    potongan_opsional = db.relationship('GajiSettingPotongan', back_populates='gaji_setting', cascade="all, delete")
    departemen = db.relationship('Departemen', back_populates='gaji_setting')

    def __repr__(self):
        return f"<GajiSetting {self.id}>"

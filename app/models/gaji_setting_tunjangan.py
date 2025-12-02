from app import db

class GajiSettingTunjangan(db.Model):
    __tablename__ = 'gaji_setting_tunjangan'

    id = db.Column(db.String(255), primary_key=True)
    gaji_setting_id = db.Column(db.String(255), db.ForeignKey('gaji_setting.id'), nullable=False)

    keterangan = db.Column(db.String(255), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

    gaji_setting = db.relationship('GajiSetting', back_populates='tunjangan_opsional')

    def __repr__(self):
        return f"<GajiSettingTunjangan {self.keterangan}>"

from app import db

class TransaksiAbsensi(db.Model):
    __tablename__ = "transaksi_absensi"

    id = db.Column(db.String(255), primary_key=True)
    id_karyawan = db.Column(
        db.String(255),
        db.ForeignKey("karyawan.id"),
        nullable=False
    )

    tanggal = db.Column(db.Date, nullable=False)
    jam_in = db.Column(db.Time, nullable=True)
    jam_out = db.Column(db.Time, nullable=True)

    foto_in = db.Column(db.String(255), nullable=True)
    foto_out = db.Column(db.String(255), nullable=True)
    longitude_in = db.Column(db.Float, nullable=True)
    latitude_in = db.Column(db.Float, nullable=True)
    longitude_out = db.Column(db.Float, nullable=True)
    latitude_out = db.Column(db.Float, nullable=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )

    karyawan = db.relationship("Karyawan", backref="absensi")

    def __repr__(self):
        return f"<Absensi {self.id_karyawan} {self.tanggal}>"

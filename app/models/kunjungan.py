from app import db
from datetime import datetime

class Kunjungan(db.Model):
    __tablename__ = "kunjungan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_karyawan = db.Column(db.String(255), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    fotos = db.relationship(
        "KunjunganFoto",
        backref="kunjungan",
        lazy=True,
        cascade="all, delete-orphan"
    )

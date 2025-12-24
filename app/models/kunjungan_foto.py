from app import db

class KunjunganFoto(db.Model):
    __tablename__ = "kunjungan_foto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kunjungan = db.Column(
        db.Integer,
        db.ForeignKey("kunjungan.id"),
        nullable=False
    )

    foto = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    jam = db.Column(db.Time, nullable=False)

from app import db

class StatusRequest(db.Model):
    __tablename__ = "status_request"

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(50), nullable=False)
    keterangan = db.Column(db.String(255))


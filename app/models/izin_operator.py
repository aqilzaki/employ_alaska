from app import db
from datetime import datetime, date

class IzinOperator(db.Model):
    __tablename__ = "izin_operator"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_karyawan = db.Column(db.String(255), db.ForeignKey("karyawan.id"), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jam = db.Column(db.Time, nullable=False)
    foto = db.Column(db.String(255))
    keterangan = db.Column(db.Text)
    id_status = db.Column(db.Integer, db.ForeignKey("status_request.id"), default=1)
    approved_by = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Relationships
    karyawan = db.relationship("Karyawan", backref="izin_operator")
    status_request = db.relationship("StatusRequest", backref="izin_operator")


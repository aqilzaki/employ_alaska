from app import db

class StatusPernikahan(db.Model):
    __tablename__ = 'status_pernikahan'

    id = db.Column(db.String(255), primary_key=True)
    nama = db.Column(db.String(255), nullable=False, unique=True)


    karyawan = db.relationship(
        "Karyawan",
        back_populates="status_pernikahan_rel"
    )
    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama
        }

    def __repr__(self):
        return f"<StatusPernikahan {self.nama}>"

from app import db

class Karyawan(db.Model):
    __tablename__ = 'karyawan'
    
    id = db.Column(db.String(255), primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    nik = db.Column(db.String(20), nullable=False, unique=True)
    id_status_pernikahan = db.Column(db.String(255), db.ForeignKey('status_pernikahan.id'), nullable=False)
    id_jabatan_karyawan = db.Column(db.String(255), db.ForeignKey('jabatan_karyawan.id'), nullable=False)
    id_departemen = db.Column(db.String(255), db.ForeignKey('departemen.id'), nullable=False)
    id_kondisi_akun = db.Column(db.String(255), db.ForeignKey('kondisi_akun.id'), nullable=False)
    id_agama = db.Column(db.String(255), db.ForeignKey('agama.id'), nullable=False)
    alamat = db.Column(db.String(255), nullable=False)
    npwp = db.Column(db.String(50), nullable=True)
    status_pajak = db.Column(db.String(50), nullable=True)
    durasi_kontrak = db.Column(db.Integer, nullable=True)
    no_hp = db.Column(db.Integer, nullable=False)
    tanggal_masuk = db.Column(db.String(255), nullable=False)
    awal_kontrak = db.Column(db.Date, nullable=False)
    akhir_kontrak = db.Column(db.Date, nullable=False)
    id_status_kerja_karyawan = db.Column(db.String(255), db.ForeignKey('status_kerja_karyawan.id'), nullable=False)
    
    # Relationships
    status_pernikahan_rel = db.relationship('StatusPernikahan', back_populates='karyawan')
    jabatan = db.relationship('Jabatan', back_populates='karyawan')
    status_kerja = db.relationship('StatusKerja', back_populates='karyawan')
    kondisi_akun = db.relationship('kondisiAkun', back_populates='karyawan')
    agama = db.relationship('Agama', back_populates='karyawan')
    departemen = db.relationship('Departemen', back_populates='karyawan')
    
    def __repr__(self):
        return f'<Karyawan {self.nama}>'
# HRIS Alaska API – Frontend Integration Guide

REST API untuk aplikasi HRIS Alaska.  
Dokumentasi ini **khusus untuk frontend** agar mudah melakukan integrasi.

---

## 🌐 Base URL

```
http://localhost:5000/api
```

---

# 📁 Endpoint Overview

Semua endpoint REST API yang tersedia:

| Module | Base Path |
|--------|-----------|
| Karyawan | `/karyawan` |
| Jabatan | `/jabatan` |
| Status Kerja | `/status-kerja` |
| Status Pernikahan | `/status-pernikahan` |
| Agama | `/agama` |
| Departemen | `/departemen` |
| Kondisi Akun | `/kondisi-akun` |
| Gaji Rule | `/gaji-rule` |
| Gaji Setting | `/gaji-setting` |

---

# 👤 Karyawan API

### **GET /karyawan**
Ambil semua data karyawan.

#### Query Params
| Param | Contoh | Deskripsi |
|-------|---------|-----------|
| `jabatan` | `?jabatan=JB01` | Filter jabatan |
| `status` | `?status=ST01` | Filter status kerja |
| `search` | `?search=aqu` | Cari nama/NIK |

---

### **GET /karyawan/{id}**
Ambil 1 karyawan berdasarkan ID.

---

### **POST /karyawan**
Tambah karyawan baru (ID auto-generate).

```json
{
  "nama": "John Doe",
  "nik": 123456789,
  "id_jabatan_karyawan": "JB01",
  "alamat": "Padang",
  "no_hp": 812345678,
  "tanggal_masuk": "2024-01-15",
  "awal_kontrak": "2024-01-15",
  "akhir_kontrak": "2025-01-15",
  "id_status_kerja_karyawan": "ST-KONT-001"
}
```

---

### **PUT /karyawan/{id}**
Update data karyawan.

---

### **DELETE /karyawan/{id}**
Hapus karyawan.

---

# 🏷️ Jabatan API

| Method | Endpoint |
|--------|----------|
| GET | `/jabatan` |
| GET | `/jabatan/{id}` |
| POST | `/jabatan` |
| PUT | `/jabatan/{id}` |
| DELETE | `/jabatan/{id}` |

---

# 💍 Status Pernikahan API

| Method | Endpoint |
|--------|----------|
| GET | `/status-pernikahan` |
| GET | `/status-pernikahan/{id}` |
| POST | `/status-pernikahan` |
| PUT | `/status-pernikahan/{id}` |
| DELETE | `/status-pernikahan/{id}` |

---

# 👔 Status Kerja API

| Method | Endpoint |
|--------|----------|
| GET | `/status-kerja` |
| GET | `/status-kerja/{id}` |
| POST | `/status-kerja` |
| PUT | `/status-kerja/{id}` |
| DELETE | `/status-kerja/{id}` |

---

# 🙏 Agama API

| Method | Endpoint |
|--------|----------|
| GET | `/agama` |
| GET | `/agama/{id}` |
| POST | `/agama` |
| PUT | `/agama/{id}` |
| DELETE | `/agama/{id}` |

---

# 🏢 Departemen API

| Method | Endpoint |
|--------|----------|
| GET | `/departemen` |
| GET | `/departemen/{id}` |
| POST | `/departemen` |
| PUT | `/departemen/{id}` |
| DELETE | `/departemen/{id}` |
| GET | `/departemen/{id}/karyawan` |

---

# 🔐 Kondisi Akun API

| Method | Endpoint |
|--------|----------|
| GET | `/kondisi-akun` |
| GET | `/kondisi-akun/{id}` |
| POST | `/kondisi-akun` |
| PUT | `/kondisi-akun/{id}` |
| DELETE | `/kondisi-akun/{id}` |

---

# 💸 Gaji Rule API

| Method | Endpoint |
|--------|----------|
| GET | `/gaji-rule` |
| GET | `/gaji-rule/{id}` |
| POST | `/gaji-rule` |
| PUT | `/gaji-rule/{id}` |
| DELETE | `/gaji-rule/{id}` |

---

# 💵 Gaji Setting API

| Method | Endpoint |
|--------|----------|
| GET | `/gaji-setting` |
| GET | `/gaji-setting/{id}` |
| POST | `/gaji-setting` |
| DELETE | `/gaji-setting/{id}` |
| GET | `/gaji-setting/{id}/hitung` |

---
🔹 Manajemen Kondisi Akun Karyawan
| Method | Endpoint                                    |
| ------ | ------------------------------------------- |
| PATCH  | `/update-kondisi-akun/<string:id_karyawan>` |
| GET    | `/get-all-karyawan-nonaktif-akun`           |

🔹 Absensi Operator & AE
📍 Absensi Operator
| Method | Endpoint                    | Keterangan                                                |
| ------ | --------------------------- | --------------------------------------------------------- |
| POST   | `/api/absensi-operator/in`  | Gunakan **Bearer Token**, form-data dengan key `foto_in`  |
| POST   | `/api/absensi-operator/out` | Gunakan **Bearer Token**, form-data dengan key `foto_out` |

📍 Absensi AE
| Method | Endpoint              | Keterangan                            |
| ------ | --------------------- | ------------------------------------- |
| POST   | `/api/absensi-ae/out` | Khusus AE dengan persyaratan tertentu |

🔹 Report Absensi
📍 Akses Umum
(Dapat diakses oleh AE, Operator, Area Eksekutif (Ketua))
| Method | Endpoint                 | Keterangan                            |
| ------ | ------------------------ | ------------------------------------- |
| GET    | `/api/absensi/report`    | Mendukung filter tanggal & departemen |
| GET    | `/api/absensi/report/me` | Report absensi milik sendiri          |

📍 Akses HRD
| Method | Endpoint                                                        | Keterangan                         |
| ------ | --------------------------------------------------------------- | ---------------------------------- |
| GET    | `/api/absensi/report?departemen={nama_departemen}`              | Filter berdasarkan departemen      |
| GET    | `/api/absensi/report?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Filter berdasarkan rentang tanggal |

📍 Akses Ketua Departemen
| Method | Endpoint                                                        | Keterangan                         |
| ------ | --------------------------------------------------------------- | ---------------------------------- |
| GET    | `/api/absensi/report?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Filter berdasarkan rentang tanggal |

🔹 Report Kunjungan AE
| Method | Endpoint                                                             | Keterangan                           |
| ------ | -------------------------------------------------------------------- | ------------------------------------ |
| GET    | `/api/kunjungan-report/AE`                                           | Akses HRD, Ketua, dan AE (pribadi)   |
| GET    | `/api/kunjungan-report/AE?tanggal=YYYY-MM-DD`                        | Filter kunjungan per hari            |
| GET    | `/api/kunjungan-report/AE?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Filter kunjungan per rentang tanggal |

🔹 Report izin 
| Method | Endpoint                                                             | Keterangan                           |
| ------ | -------------------------------------------------------------------- | ------------------------------------ |
| POST   | `/api/izin/ajukan`                                                   | Akses HRD, Ketua, dan AE (pribadi)   |
| PUT    | `/api/izin/update-status/<?id>`                                      | Akses HRD, Ketua                     |
| GET    | `/api/izin/my-history`                                               | Akses HRD, Ketua, dan AE (pribadi)   |


🔐 Authentication
Semua endpoint yang dilindungi wajib menggunakan Bearer Token
Token dikirim melalui header:
Authorization: Bearer <token>

# mssql endpoint 
| Method | Endpoint                     |
| ------ | ---------------------------- |
| GET    | `api/mssql/laporan/transaksi/bulanan` |

| Parameter       | Keterangan                       |
| --------------- | -------------------------------- |
| `bulan`         | Bulan laporan (format `YYYY-MM`) |
| `page`          | Nomor halaman                    |
| `limit`         | Jumlah data per halaman          |
| `kode_reseller` | Filter berdasarkan reseller      |
| `kode_upline`   | Filter berdasarkan upline        |

# untuk realtime endpointnya
| Method | Endpoint                      |
| ------ | ----------------------------- |
| GET    | `api/mssql/laporan/transaksi/realtime` |

| Parameter       | Keterangan                               |
| --------------- | ---------------------------------------- |
| `days`          | Jumlah hari ke belakang (default 7 hari) |
| `kode_reseller` | Filter reseller                          |
| `kode_upline`   | Filter upline                            |


# 🔥 Realtime API (SSE)

Frontend dapat menerima update realtime dari backend:

### **Connect:**
```js
const eventSource = new EventSource("http://localhost:5000/api/realtime/stream");

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Realtime:", data);
};
```

---

# ⚙️ Cara Menjalankan Backend (Untuk Frontend Dev)

```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python run.py
```

---

# 💡 Tips Frontend

- Gunakan `axios` / `fetch`
- Semua request body wajib JSON
- Untuk error, backend selalu mengirim format:
```json
{
  "success": false,
  "message": "Error message"
}
```

---

# 🎉 Selesai!
Dokumentasi ini siap dipakai frontend 🚀


# 🏢 API Karyawan Alaska

REST API untuk manajemen data karyawan Alaska yang dibangun dengan Python Flask, SQLAlchemy, dan MySQL.

## ✨ Features

- ✅ **CRUD Operations** untuk Jabatan, Status Kerja, dan Karyawan
- ✅ **Modular Architecture** (Models, DTOs, Controllers, Routes terpisah)
- ✅ **Data Validation** menggunakan Marshmallow
- ✅ **Foreign Key Relations** dengan SQLAlchemy ORM
- ✅ **Filter & Search** untuk data karyawan
- ✅ **Error Handling** yang comprehensive
- ✅ **CORS Enabled** untuk integrasi frontend

## 🛠️ Tech Stack

- **Framework:** Flask 3.0.0
- **ORM:** SQLAlchemy 3.1.1
- **Database:** MySQL/MariaDB
- **Validation:** Marshmallow 3.20.1
- **Database Driver:** PyMySQL 1.1.0
- **CORS:** Flask-CORS 4.0.0

## 📁 Project Structure

```
karyawan-alaska-api/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration settings
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── jabatan.py          # Jabatan model
│   │   ├── karyawan.py         # Karyawan model
│   │   └── status_kerja.py     # Status Kerja model
│   ├── dto/                     # Data Transfer Objects (Schemas)
│   │   ├── __init__.py
│   │   ├── jabatan_dto.py
│   │   ├── karyawan_dto.py
│   │   └── status_kerja_dto.py
│   ├── controllers/             # Business logic
│   │   ├── __init__.py
│   │   ├── jabatan_controller.py
│   │   ├── karyawan_controller.py
│   │   └── status_kerja_controller.py
│   └── routes/                  # API routes
│       ├── __init__.py
│       ├── jabatan_routes.py
│       ├── karyawan_routes.py
│       └── status_kerja_routes.py
├── .env                         # Environment variables
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── API_DOCUMENTATION.md         # API documentation
├── SETUP_GUIDE.md              # Setup & testing guide
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- MySQL/MariaDB Server
- pip (Python package manager)

### 2. Installation

```bash
# Clone atau download project
git clone <repository-url>
cd karyawan-alaska-api

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Import database menggunakan MySQL client atau phpMyAdmin
mysql -u root -p < db_karyawan_alaska.sql
```

### 4. Environment Configuration

Buat file `.env` di root folder:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=db_karyawan_alaska

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

HOST=0.0.0.0
PORT=5000
```

### 5. Run Application

```bash
python run.py
```

API akan berjalan di: `http://localhost:5000`

### 6. Test Health Check

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "OK",
  "message": "API Karyawan Alaska is running"
}
```

## 📚 API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Jabatan** |
| GET | `/jabatan` | Get all jabatan |
| GET | `/jabatan/{id}` | Get jabatan by ID |
| POST | `/jabatan` | Create new jabatan |
| PUT | `/jabatan/{id}` | Update jabatan |
| DELETE | `/jabatan/{id}` | Delete jabatan |
| **Status Kerja** |
| GET | `/status-kerja` | Get all status kerja |
| GET | `/status-kerja/{id}` | Get status kerja by ID |
| POST | `/status-kerja` | Create new status kerja |
| PUT | `/status-kerja/{id}` | Update status kerja |
| DELETE | `/status-kerja/{id}` | Delete status kerja |
| **Karyawan** |
| GET | `/karyawan` | Get all karyawan (with filters) |
| GET | `/karyawan/{id}` | Get karyawan by ID |
| POST | `/karyawan` | Create new karyawan |
| PUT | `/karyawan/{id}` | Update karyawan |
| DELETE | `/karyawan/{id}` | Delete karyawan |

### Example Request

**Create Karyawan:**
```bash
curl -X POST http://localhost:5000/api/karyawan \
  -H "Content-Type: application/json" \
  -d '{
    "id": "KAR001",
    "nama": "John Doe",
    "nik": 1234567890123456,
    "id_jabatan_karyawan": "JB01",
    "alamat": "Jl. Contoh No. 123",
    "no_hp": 628123456789,
    "tanggal_masuk": "2024-01-15",
    "awal_kontrak": "2024-01-15",
    "akhir_kontrak": "2025-01-15",
    "id_status_kerja_karyawan": "ST-KONT-003"
  }'
```

**Get Karyawan with Filter:**
```bash
# Filter by jabatan
curl http://localhost:5000/api/karyawan?jabatan=JB01

# Search by name
curl http://localhost:5000/api/karyawan?search=john

# Combined filters
curl http://localhost:5000/api/karyawan?jabatan=JB01&status=ST-KONT-001
```

Untuk dokumentasi API lengkap, lihat: **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## 🧪 Testing

Lihat panduan lengkap di: **[SETUP_GUIDE.md](SETUP_GUIDE.md)**

### Quick Test dengan cURL

```bash
# Test Jabatan
curl http://localhost:5000/api/jabatan

# Test Status Kerja
curl http://localhost:5000/api/status-kerja

# Test Karyawan
curl http://localhost:5000/api/karyawan
```

### Recommended Tools
- **Postman** - API testing
- **Thunder Client** - VS Code extension
- **Insomnia** - API client

## 🏗️ Architecture

### Modular Structure
Setiap module (Jabatan, Status Kerja, Karyawan) memiliki:
- **Model** - Database schema dan relationships
- **DTO** - Data validation dan serialization
- **Controller** - Business logic dan error handling
- **Routes** - API endpoints mapping

### Design Patterns
- **Factory Pattern** - Application initialization
- **Blueprint Pattern** - Route organization
- **Repository Pattern** - Data access abstraction
- **DTO Pattern** - Data validation dan transformation

## 🔒 Security Features

- ✅ Input validation menggunakan Marshmallow
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ Foreign key constraints
- ✅ Error handling untuk prevent information leak
- ✅ Environment variables untuk sensitive data

## 📝 Database Schema

### Tables
- **jabatan_karyawan** - Master data jabatan
- **status_kerja_karyawan** - Master data status kerja
- **karyawan** - Data karyawan dengan foreign keys

### Relationships
- Karyawan → Jabatan (Many-to-One)
- Karyawan → Status Kerja (Many-to-One)

## 🚧 Future Improvements

- [ ] Authentication & Authorization (JWT)
- [ ] Pagination untuk large datasets
- [ ] Advanced filtering & sorting
- [ ] File upload untuk foto karyawan
- [ ] Export data (Excel, PDF)
- [ ] Audit log untuk tracking changes
- [ ] Unit testing & integration testing
- [ ] API documentation dengan Swagger/OpenAPI
- [ ] Deployment guide (Docker, Heroku, AWS)

## 🐛 Troubleshooting

### Common Issues

**1. Cannot connect to MySQL**
```bash
# Check MySQL service status
# Windows (XAMPP):
- Buka XAMPP Control Panel
- Start Apache & MySQL

# Check connection
mysql -u root -p
```

**2. Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**3. Port already in use**
```bash
# Change port in .env
PORT=5001
```

Untuk troubleshooting lengkap, lihat: **[SETUP_GUIDE.md](SETUP_GUIDE.md)**

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**API Karyawan Alaska**
- Framework: Flask (Python)
- Database: MySQL/MariaDB
- Architecture: Modular REST API

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

Jika ada pertanyaan atau masalah:
- Cek dokumentasi di folder project
- Buat issue di repository
- Contact: [your-email@example.com]

---

**Happy Coding! 🎉**
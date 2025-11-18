// File: src/admin/components/EditEmployeeModal.jsx
// Versi ini memperbaiki validasi "NIK sudah terdaftar"

import React, { useState, useEffect } from 'react';
import Modal from '../../components/ui/Modal';

// Helper (Sudah benar)
const formatDateForInput = (dateStr) => {
  if (!dateStr) return '';
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr; 
    return date.toISOString().split('T')[0];
  } catch (e) {
    return dateStr;
  }
};


export default function EditEmployeeModal({ 
  isOpen, 
  onClose, 
  onUpdateEmployee,
  employeeData,   
  jabatanOptions,
  statusKerjaOptions 
}) {
  
  const [formData, setFormData] = useState({
    nama: '', nik: '', id_jabatan_karyawan: '', alamat: '',
    no_hp: '', tanggal_masuk: '', awal_kontrak: '',
    akhir_kontrak: '', id_status_kerja_karyawan: '',
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // useEffect (Sudah benar)
  useEffect(() => {
    if (isOpen && employeeData) {
      setError(null);
      setFormData({
        nama: employeeData.nama || '',
        nik: employeeData.nik || '',
        id_jabatan_karyawan: String(employeeData.id_jabatan_karyawan || ''),
        alamat: employeeData.alamat || '',
        no_hp: employeeData.no_hp || '',
        tanggal_masuk: formatDateForInput(employeeData.tanggal_masuk),
        awal_kontrak: formatDateForInput(employeeData.awal_kontrak),
        akhir_kontrak: formatDateForInput(employeeData.akhir_kontrak),
        id_status_kerja_karyawan: String(employeeData.id_status_kerja_karyawan || ''),
      });
    }
  }, [isOpen, employeeData]); 


  // Handle change (Sudah benar)
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ 
      ...prev, 
      [name]: value 
    }));
  };

  // Handle submit (INI YANG DIUBAH)
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    // Helper (Sudah benar)
    const parseNumberOrNull = (value) => {
      if (value === null || value === undefined || String(value).trim() === '') {
        return null;
      }
      const num = Number(value); 
      return isNaN(num) ? null : num;
    };
    
    // Ini data dari form (termasuk nama yg diubah)
    const dataToSubmit = {
      ...formData,
      id: undefined, 
      tanggal_masuk: formData.tanggal_masuk === '' ? null : formData.tanggal_masuk,
      awal_kontrak: formData.awal_kontrak === '' ? null : formData.awal_kontrak,
      akhir_kontrak: formData.akhir_kontrak === '' ? null : formData.akhir_kontrak,
    };

    // ==========================================================
    // PERBAIKAN DI SINI:
    // Cek apakah NIK atau No. HP diubah. Kalo gak, JANGAN DIKIRIM.
    // ==========================================================
    
    // Konversi NIK (form) dan NIK (original) ke tipe yang sama
    const formNik = parseNumberOrNull(formData.nik);
    const originalNik = parseNumberOrNull(employeeData.nik);
    
    // Jika NIK di form SAMA kayak NIK aslinya, HAPUS 'nik' dari data kiriman
    if (formNik === originalNik) {
      delete dataToSubmit.nik; // <-- BIANG KELADINYA DI SINI
    } else {
      dataToSubmit.nik = formNik; // Kalo beda, baru kirim
    }
    
    // Lakukan hal yang sama untuk no_hp (buat jaga-jaga)
    const formNoHp = parseNumberOrNull(formData.no_hp);
    const originalNoHp = parseNumberOrNull(employeeData.no_hp);
    
    if (formNoHp === originalNoHp) {
      delete dataToSubmit.no_hp;
    } else {
      dataToSubmit.no_hp = formNoHp;
    }
    // ==========================================================

    try {
      // Kirim data yang sudah dibersihkan
      await onUpdateEmployee(employeeData.id, dataToSubmit); 

    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal title="Edit Karyawan" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            Gagal mengupdate: {error}
          </div>
        )}

        {/* ... (Semua field form di bawah ini sudah benar) ... */}
        
        {/* Baris 1: Nama & NIK */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Nama Lengkap</label>
            <input
              type="text"
              name="nama"
              value={formData.nama}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
              required
            />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">NIK</label>
            <input
              type="number"
              name="nik"
              value={formData.nik}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
              placeholder="Contoh: 13710..."
            />
          </div>
        </div>
        
        {/* Baris 2: Jabatan & No. HP */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Jabatan</label>
            <select
              name="id_jabatan_karyawan"
              value={formData.id_jabatan_karyawan}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
              disabled={jabatanOptions.length === 0}
            >
              {jabatanOptions.map(jabatan => (
                <option key={jabatan.id} value={jabatan.id}>
                  {jabatan.nama_jabatan || jabatan.nama}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">No. HP</label>
            <input
              type="number"
              name="no_hp"
              value={formData.no_hp}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
              placeholder="Contoh: 0812..."
            />
          </div>
        </div>
        
        {/* Baris 3: Alamat */}
        <div>
          <label className="text-sm font-medium text-gray-700 block mb-1">Alamat</label>
          <textarea
            name="alamat"
            value={formData.alamat}
            onChange={handleChange}
            rows="2"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
          ></textarea>
        </div>
        
        {/* Baris 4: Tanggal Masuk & Status */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Tanggal Masuk</label>
            <input
              type="date"
              name="tanggal_masuk"
              value={formData.tanggal_masuk}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Status Kerja</label>
            <select
              name="id_status_kerja_karyawan"
              value={formData.id_status_kerja_karyawan}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
              disabled={statusKerjaOptions.length === 0}
            >
              {statusKerjaOptions.map(status => (
                <option key={status.id} value={status.id}>
                  {status.nama_status || status.nama}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Baris 5: Kontrak */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Awal Kontrak</label>
            <input
              type="date"
              name="awal_kontrak"
              value={formData.awal_kontrak}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">Akhir Kontrak</label>
            <input
              type="date"
              name="akhir_kontrak"
              value={formData.akhir_kontrak}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#800020]"
            />
          </div>
        </div>

        {/* Tombol */}
        <div className="pt-4 flex justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
          >
            Batal
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 bg-linear-to-r from-[#800020] to-[#a0002a] text-white rounded-lg hover:shadow-lg disabled:opacity-50"
          >
            {isSubmitting ? 'Mengupdate...' : 'Update Karyawan'}
          </button>
        </div>
      </form>
    </Modal>
  );
}

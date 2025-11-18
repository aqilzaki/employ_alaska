// File: src/components/ui/Modal.jsx

import React from 'react';
import { X } from 'lucide-react';

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) {
    return null; // Jangan render apapun jika tidak 'isOpen'
  }

  return (
    // 1. Backdrop (overlay gelap)
    <div
      onClick={onClose} // Menutup modal saat backdrop diklik
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
    >
      {/* 2. Konten Modal */}
      <div
        onClick={(e) => e.stopPropagation()} // Mencegah modal tertutup saat diklik di dalam konten
        className="bg-white rounded-2xl shadow-xl w-full max-w-md"
      >
        {/* 3. Header Modal */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-xl font-bold text-gray-800">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full p-1 transition-all"
          >
            <X size={20} />
          </button>
        </div>

        {/* 4. Body Modal (tempat form kita nanti) */}
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
}
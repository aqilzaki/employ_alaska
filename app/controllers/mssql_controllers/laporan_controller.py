from flask import jsonify, request
from datetime import date
from calendar import monthrange
from app.utils.mssql import get_mssql_conn


class LaporanController:

    @staticmethod
    def get_laporan_transaksi():
        # ===== AMBIL PARAM =====
        start_date = request.args.get("from")
        end_date = request.args.get("to")
        bulan = request.args.get("bulan")  # optional: YYYY-MM

        # ===== RESOLVE TANGGAL =====
        if bulan:
            year, month = map(int, bulan.split("-"))
            start_date = date(year, month, 1)
            end_date = date(year, month, monthrange(year, month)[1])
        elif start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
        else:
            return jsonify({
                "success": False,
                "message": "Isi parameter 'from' & 'to' atau 'bulan' (YYYY-MM)"
            }), 400

        # ===== QUERY MSSQL =====
        query = """
            SELECT
                t.tgl_status,
                t.kode_reseller,
                r.nama                AS nama_reseller,
                r.kode_upline         AS kode_upline,
                ru.nama               AS nama_upline,
                t.harga,
                t.harga_beli,
                t.harga_beli2,
                t.komisi,
                t.status,
                ISNULL(t.harga, 0) - ISNULL(t.harga_beli, 0) AS laba
            FROM transaksi t
            LEFT JOIN reseller r
                ON r.kode = t.kode_reseller
            LEFT JOIN reseller ru
                ON ru.kode = r.kode_upline
            WHERE t.tgl_status >= ?
              AND t.tgl_status < DATEADD(day, 1, ?)
              AND (t.status = 20 OR t.status = '20')
              AND t.harga <> 0
            ORDER BY t.tgl_status
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()

        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()

        # ===== CONVERT KE JSON =====
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Data laporan transaksi berhasil diambil",
            "total_data": len(data),
            "data": data
        }), 200

from flask import jsonify, request
from app.database.mssql import get_mssql_conn

class MSSQLMutasiController:

    @staticmethod
    def get_by_reseller():
        kode_reseller = request.args.get("kode_reseller")
        limit = int(request.args.get("limit", 20))

        if not kode_reseller:
            return jsonify({
                "success": False,
                "message": "kode_reseller wajib"
            }), 400

        conn = get_mssql_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT TOP (?)
                kode,
                kode_reseller,
                tanggal,
                jumlah,
                keterangan,
                jenis,
                kode_transaksi,
                saldo_akhir
            FROM dbo.mutasi
            WHERE kode_reseller = ?
            ORDER BY tanggal DESC
        """, limit, kode_reseller)

        rows = cursor.fetchall()
        conn.close()

        data = [
            {
                "kode": r[0],
                "kode_reseller": r[1],
                "tanggal": str(r[2]),
                "jumlah": float(r[3]),
                "keterangan": r[4],
                "jenis": r[5],
                "kode_transaksi": r[6],
                "saldo_akhir": float(r[7])
            }
            for r in rows
        ]

        return jsonify({
            "success": True,
            "source": "mssql",
            "count": len(data),
            "data": data
        }), 200

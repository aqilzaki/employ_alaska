from flask import jsonify, request
from datetime import date
from calendar import monthrange
from app.database.mssql import get_mssql_conn
# helpers
def to_float(val, default=0.0):
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

class MSSQLTransaksiController:

    @staticmethod
    def _resolve_periode(bulan: str):
        year, month = map(int, bulan.split("-"))
        today = date.today()

        start_date = date(year, month, 1)
        if year == today.year and month == today.month:
            end_date = today
            realtime = True
        else:
            end_date = date(year, month, monthrange(year, month)[1])
            realtime = False

        return start_date, end_date, realtime

    @staticmethod
    def get_all_realtime_by_bulan():
     bulan = request.args.get("bulan")  # YYYY-MM

     if not bulan:
            return jsonify({
                "success": False,
                "message": "bulan wajib (YYYY-MM)"
            }), 400

     try:
            start_date, end_date, realtime = MSSQLTransaksiController._resolve_periode(bulan)
     except Exception:
            return jsonify({
                "success": False,
                "message": "Format bulan harus YYYY-MM"
            }), 400

     conn = get_mssql_conn()
     cursor = conn.cursor()

     cursor.execute("""
        SELECT
            r.kode        AS kode_reseller,
            r.nama        AS nama_reseller,
            t.tgl_status,
            t.kode        AS kode_transaksi,
            t.kode_produk,
            t.tujuan,
            t.harga,
            t.harga_beli,
            t.harga_beli2,
            ISNULL(t.harga, 0) - ISNULL(t.harga_beli2, t.harga_beli) AS laba,
            t.komisi,
            t.status
        FROM transaksi t
        JOIN reseller r ON r.kode = t.kode_reseller
        WHERE
            ISNULL(r.deleted, 0) = 0
            AND (r.kode_upline IS NULL OR r.kode_upline IN ('', '0', '-', 'ROOT'))
            AND t.tgl_status >= ?
            AND t.tgl_status < DATEADD(day, 1, ?)
        ORDER BY t.tgl_status DESC
        """, start_date, end_date)

     rows = cursor.fetchall()
     conn.close()

     data = [
            {
                 "kode_reseller": r[0],
        "nama_reseller": r[1],
        "tgl_status": str(r[2]),
        "kode_transaksi": r[3],
        "kode_produk": r[4],
        "tujuan": r[5],
        "harga": to_float(r[6]),
        "harga_beli": to_float(r[7]),
        "harga_beli2": to_float(r[8]),
        "laba": to_float(r[9]),
        "komisi": to_float(r[10]),
        "status": r[11],
            }
            for r in rows
        ]

     return jsonify({
            "success": True,
            "realtime": realtime,
            "periode": {
                "bulan": bulan,
                "start": str(start_date),
                "end": str(end_date)
            },
            "count": len(data),
            "data": data
        }), 200


    @staticmethod
    def get_by_id_realtime_by_bulan(kode_transaksi):
        kode_reseller = request.args.get("kode_reseller")
        bulan = request.args.get("bulan")  # YYYY-MM

        if not kode_reseller or not bulan:
            return jsonify({
                "success": False,
                "message": "kode_reseller dan bulan wajib (YYYY-MM)"
            }), 400

        try:
            start_date, end_date, realtime = MSSQLTransaksiController._resolve_periode(bulan)
        except Exception:
            return jsonify({
                "success": False,
                "message": "Format bulan harus YYYY-MM"
            }), 400

        conn = get_mssql_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
              t.tgl_status,
              t.kode,
              t.kode_produk,
              t.tujuan,
              t.pengirim,
              t.tipe_pengirim,
              t.kode_reseller,
              t.harga,
              t.harga_beli,
              t.harga_beli2,
              t.komisi,
              t.status
            FROM transaksi t
            WHERE t.kode = ?
              AND t.kode_reseller = ?
              AND t.tgl_status >= ?
              AND t.tgl_status < DATEADD(day, 1, ?)
              AND (t.status = 20 OR t.status = '20')
              AND t.harga <> 0
        """, kode_transaksi, kode_reseller, start_date, end_date)

        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({
                "success": False,
                "message": "Transaksi tidak ditemukan pada periode tersebut"
            }), 404

        data = {
            "tgl_status": str(row[0]),
            "kode": row[1],
            "kode_produk": row[2],
            "tujuan": row[3],
            "pengirim": row[4],
            "tipe_pengirim": row[5],
            "kode_reseller": row[6],
            "harga": float(row[7]),
            "harga_beli": float(row[8]),
            "harga_beli2": float(row[9]),
            "komisi": float(row[10]),
            "status": row[11],
        }

        return jsonify({
            "success": True,
            "realtime": realtime,
            "periode": {
                "bulan": bulan,
                "start": str(start_date),
                "end": str(end_date)
            },
            "data": data
        }), 200

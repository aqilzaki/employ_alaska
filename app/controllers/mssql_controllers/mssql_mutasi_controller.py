from flask import jsonify, request
from datetime import date, timedelta
from calendar import monthrange
from app.utils.mssql import get_mssql_conn


class LaporanTestController:

    # =====================================================
    # 📌 LAPORAN BULANAN (HISTORICAL)
    # =====================================================
    @staticmethod
    def transaksi_bulanan():
        bulan = request.args.get("bulan")           # YYYY-MM
        kode_reseller = request.args.get("kode_reseller")
        kode_upline = request.args.get("kode_upline")

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
        offset = (page - 1) * limit

        if not bulan:
            return jsonify({
                "success": False,
                "message": "Parameter bulan wajib (YYYY-MM)"
            }), 400

        year, month = map(int, bulan.split("-"))
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])

        filters = []
        params = [start_date, end_date]

        if kode_reseller:
            filters.append("t.kode_reseller = ?")
            params.append(kode_reseller)

        if kode_upline:
            filters.append("r.kode_upline = ?")
            params.append(kode_upline)

        where_extra = ""
        if filters:
            where_extra = " AND " + " AND ".join(filters)

        query = f"""
            SELECT
                t.tgl_status,
                t.kode_reseller,
                r.nama AS nama_reseller,
                r.kode_upline,
                ru.nama AS nama_upline,
                t.harga,
                t.harga_beli,
                t.harga_beli2,
                t.komisi,
                ISNULL(t.harga,0) - ISNULL(t.harga_beli,0) AS laba
            FROM transaksi t
            LEFT JOIN reseller r ON r.kode = t.kode_reseller
            LEFT JOIN reseller ru ON ru.kode = r.kode_upline
            WHERE t.tgl_status >= ?
              AND t.tgl_status < DATEADD(day,1,?)
              AND (t.status = 20 OR t.status = '20')
              AND t.harga <> 0
              {where_extra}
            ORDER BY t.tgl_status
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """

        count_query = f"""
            SELECT
                COUNT(*) AS total_data,
                SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS total_laba
            FROM transaksi t
            LEFT JOIN reseller r ON r.kode = t.kode_reseller
            WHERE t.tgl_status >= ?
              AND t.tgl_status < DATEADD(day,1,?)
              AND (t.status = 20 OR t.status = '20')
              AND t.harga <> 0
              {where_extra}
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()

        # data
        cursor.execute(query, params + [offset, limit])
        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # summary
        cursor.execute(count_query, params)
        summary = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "bulan": bulan,
            "page": page,
            "limit": limit,
            "total_data": summary.total_data or 0,
            "total_laba": summary.total_laba or 0,
            "data": data
        }), 200

    # =====================================================
    # ⚡ REALTIME TRANSAKSI (HARI INI / 7 HARI TERAKHIR)
    # =====================================================
    @staticmethod
    def transaksi_realtime():
        days = int(request.args.get("days", 7))  # default 7 hari
        kode_reseller = request.args.get("kode_reseller")
        kode_upline = request.args.get("kode_upline")

        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        filters = []
        params = [start_date, end_date]

        if kode_reseller:
            filters.append("t.kode_reseller = ?")
            params.append(kode_reseller)

        if kode_upline:
            filters.append("r.kode_upline = ?")
            params.append(kode_upline)

        where_extra = ""
        if filters:
            where_extra = " AND " + " AND ".join(filters)

        query = f"""
            SELECT
                t.tgl_status,
                t.kode_reseller,
                r.nama AS nama_reseller,
                r.kode_upline,
                ru.nama AS nama_upline,
                t.harga,
                t.harga_beli,
                ISNULL(t.harga,0) - ISNULL(t.harga_beli,0) AS laba
            FROM transaksi t
            LEFT JOIN reseller r ON r.kode = t.kode_reseller
            LEFT JOIN reseller ru ON ru.kode = r.kode_upline
            WHERE t.tgl_status >= ?
              AND t.tgl_status < DATEADD(day,1,?)
              AND (t.status = 20 OR t.status = '20')
              AND t.harga <> 0
              {where_extra}
            ORDER BY t.tgl_status DESC
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "mode": "realtime",
            "range_hari": days,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "total_data": len(data),
            "data": data
        }), 200

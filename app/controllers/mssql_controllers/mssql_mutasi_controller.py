from flask import jsonify, request
from datetime import date, timedelta
from calendar import monthrange
from app.utils.mssql import get_mssql_conn
from datetime import datetime
import math

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
        days = int(request.args.get("days", 0))  # default 7 hari
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


# =====================================================
#  laporan pivot
# ====================================================

class LaporanPivotController:
    @staticmethod
    def pivot_laba_reseller():
        start = request.args.get("start")
        end = request.args.get("end")

        if not start or not end:
            return jsonify({
                "success": False,
                "message": "Parameter start dan end wajib"
            }), 400

        query = """
            SELECT
                t.kode_reseller,
                r.nama AS nama_reseller,
                SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS total_laba
            FROM transaksi t
            LEFT JOIN reseller r ON r.kode = t.kode_reseller
            WHERE t.tgl_status >= ?
            AND t.tgl_status < DATEADD(day,1,?)
            AND (t.status = 20 OR t.status = '20')
            AND t.harga <> 0
            GROUP BY t.kode_reseller, r.nama
            ORDER BY total_laba DESC
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()
        cursor.execute(query, (start, end))

        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "data": data
        }), 200
    

    @staticmethod
    def pivot_laba_upline():
        start = request.args.get("start")
        end = request.args.get("end")

        if not start or not end:
            return jsonify({
                "success": False,
                "message": "Parameter start dan end wajib"
            }), 400

        query = """
            SELECT
                r.kode_upline,
                ru.nama AS nama_upline,
                SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS total_laba
            FROM transaksi t
            LEFT JOIN reseller r ON r.kode = t.kode_reseller
            LEFT JOIN reseller ru ON ru.kode = r.kode_upline
            WHERE t.tgl_status >= ?
            AND t.tgl_status < DATEADD(day,1,?)
            AND (t.status = 20 OR t.status = '20')
            AND t.harga <> 0
            AND r.kode_upline IS NOT NULL
            GROUP BY r.kode_upline, ru.nama
            ORDER BY total_laba DESC
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()
        cursor.execute(query, (start, end))

        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "data": data
        }), 200

    @staticmethod
    def pivot_laba_harian():
        """
        Pivot laba harian:
        - Default: hari terbaru (hari ini)
        - Bisa filter manual: ?start=YYYY-MM-DD&end=YYYY-MM-DD
        """

        start = request.args.get("start")
        end = request.args.get("end")

        # ===============================
        # 1. Tentukan range tanggal
        # ===============================
        if start and end:
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "Format tanggal harus YYYY-MM-DD"
                }), 400
        else:
            # Default → hari ini
            start_date = date.today()
            end_date = date.today()

        # ===============================
        # 2. Query MSSQL
        # ===============================
        query = """
            SELECT
                CAST(t.tgl_status AS DATE) AS tanggal,
                SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS total_laba
            FROM transaksi t
            WHERE t.tgl_status >= ?
            AND t.tgl_status < DATEADD(day,1,?)
            AND (t.status = 20 OR t.status = '20')
            AND t.harga <> 0
            GROUP BY CAST(t.tgl_status AS DATE)
            ORDER BY tanggal
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))

        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        # ===============================
        # 3. Response
        # ===============================
        return jsonify({
            "success": True,
            "range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "data": data
        }), 200

    @staticmethod
    def pivot_laba_bulanan():
        start = request.args.get("start")
        end = request.args.get("end")

        if not start or not end:
            return jsonify({
                "success": False,
                "message": "Parameter start dan end wajib"
            }), 400

        query = """
            SELECT
                FORMAT(t.tgl_status, 'yyyy-MM') AS bulan,
                SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS total_laba
            FROM transaksi t
            WHERE t.tgl_status >= ?
            AND t.tgl_status < DATEADD(day,1,?)
            AND (t.status = 20 OR t.status = '20')
            AND t.harga <> 0
            GROUP BY FORMAT(t.tgl_status, 'yyyy-MM')
            ORDER BY bulan
        """

        conn = get_mssql_conn()
        cursor = conn.cursor()
        cursor.execute(query, (start, end))

        rows = cursor.fetchall()
        columns = [c[0] for c in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "data": data
        }), 200



    @staticmethod
    def pivot_laba():
        """
        Pivot laporan laba:
        - Per reseller
        - Per upline
        - Per hari (kolom dinamis)
        - Grand total
        - Pagination (server-side slice)
        """

        # ===============================
        # Query Params
        # ===============================
        start = request.args.get("start")
        end = request.args.get("end")

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))

        if not start or not end:
            return jsonify({
                "success": False,
                "message": "Parameter start dan end wajib diisi (YYYY-MM-DD)"
            }), 400

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Format tanggal harus YYYY-MM-DD"
            }), 400

        conn = get_mssql_conn()
        cursor = conn.cursor()

        # ===============================
        # 1. Generate kolom tanggal
        # ===============================
        col_query = """
            SELECT DISTINCT CAST(tgl_status AS date) AS tgl
            FROM transaksi
            WHERE tgl_status >= ?
            AND tgl_status < DATEADD(day, 1, ?)
            ORDER BY tgl
        """

        cursor.execute(col_query, (start_date, end_date))
        dates = [row[0] for row in cursor.fetchall()]

        if not dates:
            return jsonify({
                "success": True,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total_rows": 0,
                    "total_pages": 0
                },
                "data": []
            })

        cols = []
        for d in dates:
            label = d.strftime("%d-%b")
            cols.append(f"""
                SUM(
                    CASE 
                        WHEN CAST(t.tgl_status AS date) = '{d}'
                        THEN ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)
                        ELSE 0
                    END
                ) AS [{label}]
            """)

        cols_sql = ",\n".join(cols)

        # ===============================
        # 2. SQL Pivot Final
        # ===============================
        sql = f"""
        SELECT
            CASE 
                WHEN GROUPING(r.kode_upline) = 1 THEN 'GRAND TOTAL'
                ELSE r.kode_upline
            END AS kode_upline,

            CASE
                WHEN GROUPING(t.kode_reseller) = 1 
                    AND GROUPING(r.kode_upline) = 0
                    THEN 'TOTAL UPLINE'
                WHEN GROUPING(t.kode_reseller) = 1 
                    AND GROUPING(r.kode_upline) = 1
                    THEN 'TOTAL ALL'
                ELSE t.kode_reseller
            END AS kode_reseller,

            MAX(r.nama) AS nama_reseller,

            {cols_sql},

            SUM(ISNULL(t.harga,0) - ISNULL(t.harga_beli,0)) AS grand_total

        FROM transaksi t
        LEFT JOIN reseller r ON r.kode = t.kode_reseller

        WHERE t.tgl_status >= ?
        AND t.tgl_status < DATEADD(day, 1, ?)
        AND (t.status = 20 OR t.status = '20')
        AND t.harga <> 0

        GROUP BY GROUPING SETS (
            (r.kode_upline, t.kode_reseller),
            (r.kode_upline),
            ()
        )

        ORDER BY
            GROUPING(r.kode_upline),
            r.kode_upline,
            GROUPING(t.kode_reseller),
            t.kode_reseller
        """

        cursor.execute(sql, (start_date, end_date))

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        # ===============================
        # 3. Pagination (Python slice)
        # ===============================
        total_rows = len(data)
        total_pages = math.ceil(total_rows / limit)

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        paginated_data = data[start_idx:end_idx]

        # ===============================
        # 4. Response
        # ===============================
        return jsonify({
            "success": True,
            "meta": {
                "start": start,
                "end": end,
                "page": page,
                "limit": limit,
                "total_rows": total_rows,
                "total_pages": total_pages
            },
            "data": paginated_data
        })

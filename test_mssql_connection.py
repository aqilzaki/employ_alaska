from app.database.mssql import get_mssql_conn

conn = get_mssql_conn()
cursor = conn.cursor()

cursor.execute("""
    SELECT top 5 *
    FROM dbo.mutasi
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

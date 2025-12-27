from app.utils.mssql import get_mssql_conn

conn = get_mssql_conn()
print("MSSQL CONNECTED")
conn.close()
print("MSSQL CONNECTION CLOSED")
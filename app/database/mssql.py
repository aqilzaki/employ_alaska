import pyodbc

def get_mssql_conn():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=36.64.102.226,1433;"
        "DATABASE=otomax;"
        "UID=Aqil01;"
        "PWD=Hidupprabowo66;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

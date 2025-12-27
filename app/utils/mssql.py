import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_mssql_conn():
    conn_str = (
        f"DRIVER={{{os.getenv('MSSQL_DRIVER')}}};"
        f"SERVER={os.getenv('MSSQL_HOST')},{os.getenv('MSSQL_PORT')};"
        f"DATABASE={os.getenv('MSSQL_DB')};"
        f"UID={os.getenv('MSSQL_USER')};"
        f"PWD={os.getenv('MSSQL_PASSWORD')};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

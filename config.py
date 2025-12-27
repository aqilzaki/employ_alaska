import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    MSSQL_DRIVER = os.getenv("MSSQL_DRIVER")
    MSSQL_HOST = os.getenv("MSSQL_HOST")
    MSSQL_PORT = os.getenv("MSSQL_PORT")
    MSSQL_DB = os.getenv("MSSQL_DB")
    MSSQL_USER = os.getenv("MSSQL_USER")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
    MSSQL_ENCRYPT = os.getenv("MSSQL_ENCRYPT")
    MSSQL_TRUST_CERT = os.getenv("MSSQL_TRUST_CERT")



    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60


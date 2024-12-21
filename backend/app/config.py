# config.py

import pyodbc
from pymongo import MongoClient
import urllib.parse

class Config:
    SQL_SERVER_HOST = '192.168.35.129'
    SQL_SERVER_PORT = 1433
    SQL_SERVER_USER = 'myuser'
    SQL_SERVER_PASSWORD = 'User@123456'
    SQL_SERVER_DB = 'MyDatabase'
    SQL_SERVER_DRIVER = '{ODBC Driver 17 for SQL Server}'

    MONGO_USER = "myuser2"
    MONGO_PASSWORD = "User2@123456"
    AUTH_SOURCE = "mydb"  # 认证数据库
    MONGO_DB_NAME = "mydb"  # 目标数据库

    # URL 编码用户名和密码
    ENCODED_USER = urllib.parse.quote_plus(MONGO_USER)
    ENCODED_PASSWORD = urllib.parse.quote_plus(MONGO_PASSWORD)

    # 构建 MongoDB URI
    MONGO_URI = f"mongodb://{ENCODED_USER}:{ENCODED_PASSWORD}@192.168.35.129:27017/?authSource={AUTH_SOURCE}"

    @staticmethod
    def get_sql_server_connection():
        conn = pyodbc.connect(
            driver=Config.SQL_SERVER_DRIVER,
            server=Config.SQL_SERVER_HOST,
            port=Config.SQL_SERVER_PORT,
            database=Config.SQL_SERVER_DB,
            user=Config.SQL_SERVER_USER,
            password=Config.SQL_SERVER_PASSWORD,
        )
        return conn

    @staticmethod
    def get_mongo_client():
        """获取 MongoDB 客户端"""
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI)
        return client[Config.MONGO_DB_NAME]

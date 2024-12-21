# test_sql_server.py

import sys
import os

# 添加项目根目录到 Python 搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pyodbc
from backend.app.config import Config

def test_sql_server_connection():
    try:
        conn = pyodbc.connect(
            driver=Config.SQL_SERVER_DRIVER,
            server=Config.SQL_SERVER_HOST,
            port=Config.SQL_SERVER_PORT,
            database=Config.SQL_SERVER_DB,
            user=Config.SQL_SERVER_USER,
            password=Config.SQL_SERVER_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # 测试简单查询
        result = cursor.fetchone()
        conn.close()
        print("SQL Server 连接成功:", result)
    except Exception as e:
        print("SQL Server 连接失败:", e)

if __name__ == "__main__":
    test_sql_server_connection()

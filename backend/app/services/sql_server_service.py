# backend/app/services/sql_server_service.py
import pyodbc
from backend.app.config import Config

class SQLServerDatabaseManager:
    _connection = None

    @classmethod
    def get_connection(cls):
        """
        获取全局数据库连接。如果不存在，则创建一个新连接。
        """
        if cls._connection is None:
            cls._connection = pyodbc.connect(
                driver=Config.SQL_SERVER_DRIVER,
                server=Config.SQL_SERVER_HOST,
                port=Config.SQL_SERVER_PORT,
                database=Config.SQL_SERVER_DB,
                user=Config.SQL_SERVER_USER,
                password=Config.SQL_SERVER_PASSWORD
            )
        return cls._connection

    @classmethod
    def close_connection(cls):
        """
        关闭全局数据库连接。
        """
        if cls._connection:
            cls._connection.close()
            cls._connection = None


def create_table(query: str):
    """
    创建表并打印连接的 SQL Server 实例和当前数据库。
    """
    try:
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 打印 SQL Server 实例的唯一标识符
        cursor.execute("SELECT @@SERVERNAME AS ServerName;")
        server_name = cursor.fetchone()
        print("Connected to SQL Server instance:", server_name[0])

        # 打印当前连接的数据库名称
        cursor.execute("SELECT DB_NAME() AS CurrentDatabase;")
        current_db = cursor.fetchone()
        print("Connected to database:", current_db[0])

        # 执行创建表的 SQL 语句
        cursor.execute(query)
        conn.commit()

        print(f"Table creation query executed successfully in database {current_db[0]} on server {server_name[0]}.")
        return {
            "status": "success",
            "message": f"Table created successfully in database {current_db[0]} on server {server_name[0]}"
        }
    except Exception as e:
        print("Error during table creation:", e)
        return {"status": "error", "message": str(e)}


def insert_data(table_name: str, columns: list, values: list):
    """
    向指定表插入数据，不使用 dict 或键值对。
    """
    try:
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 动态生成 SQL 插入语句
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        # 打印调试信息
        print("Generated Query:", query)
        print("Data Values (list):", values)

        # 执行插入语句
        cursor.execute(query, values)
        conn.commit()

        return {"status": "success", "message": f"Data inserted into table '{table_name}' successfully."}
    except Exception as e:
        print("Error during data insertion:", e)
        return {"status": "error", "message": str(e)}


def delete_data(table_name: str, condition: str):
    """
    删除指定表中满足条件的数据。
    :param table_name: 表名
    :param condition: 删除条件（WHERE 子句）
    """
    try:
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 动态生成 DELETE SQL 语句
        query = f"DELETE FROM {table_name} WHERE {condition}"

        # 打印调试信息
        print("Generated Query:", query)

        # 执行删除操作
        cursor.execute(query)
        conn.commit()

        return {"status": "success", "message": f"Data deleted from table '{table_name}' successfully."}
    except Exception as e:
        print("Error during data deletion:", e)
        return {"status": "error", "message": str(e)}

def update_data(table_name: str, condition: str, updates: list):
    """
    更新指定表中的数据。
    :param table_name: 表名
    :param condition: 更新条件
    :param updates: 更新操作列表，例如 ["column1 = value1", "column2 = value2"]
    """
    try:
        # 获取数据库连接
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 动态生成 SQL 更新语句
        updates_str = ", ".join(updates)
        query = f"UPDATE {table_name} SET {updates_str} WHERE {condition}"

        # 打印调试信息
        print("Generated Query:", query)

        # 执行更新操作
        cursor.execute(query)
        conn.commit()

        return {"status": "success", "message": f"Data in table '{table_name}' updated successfully."}
    except Exception as e:
        print("Error during data update:", e)
        return {"status": "error", "message": str(e)}

def delete_table(table_name: str):
    """
    删除指定数据表。
    """
    try:
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 动态生成删除表的 SQL 语句
        query = f"DROP TABLE {table_name}"

        # 打印调试信息
        print("Generated Query:", query)

        # 执行删除表的操作
        cursor.execute(query)
        conn.commit()

        return {"status": "success", "message": f"Table '{table_name}' deleted successfully."}
    except Exception as e:
        print("Error during table deletion:", e)
        return {"status": "error", "message": str(e)}

def join_tables(query: str):
    """
    执行跨表 JOIN 查询。
    :param query: 完整的 SQL 查询语句（如 JOIN 操作）。
    """
    try:
        conn = SQLServerDatabaseManager.get_connection()
        cursor = conn.cursor()

        # 打印调试信息
        print("Generated Query:", query)

        # 执行查询
        cursor.execute(query)
        results = cursor.fetchall()

        # 获取列名
        columns = [column[0] for column in cursor.description]

        # 将结果转换为字典格式
        result_data = [dict(zip(columns, row)) for row in results]

        return {"status": "success", "data": result_data}
    except Exception as e:
        print("Error during JOIN operation:", e)
        return {"status": "error", "message": str(e)}






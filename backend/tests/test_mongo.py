import sys
import os

# 添加项目根目录到 Python 搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pymongo import MongoClient
from backend.app.config import Config

def test_mongo_connection():
    try:
        # 获取 MongoDB 客户端
        client = MongoClient(Config.MONGO_URI)
        # 选择数据库
        db = client[Config.MONGO_DB_NAME]
        # 测试获取集合列表
        collections = db.list_collection_names()
        print("MongoDB 连接成功, 集合列表:", collections)
    except Exception as e:
        print("MongoDB 连接失败:", e)

if __name__ == "__main__":
    test_mongo_connection()

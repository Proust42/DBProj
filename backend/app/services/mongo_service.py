from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from backend.app.config import Config


class MongoService:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]

    def create_collection(self, collection_name, indexes=None):
        """
        创建集合，并可选配置索引。

        :param collection_name: 集合名称
        :param indexes: 索引配置列表（可选），每个元素为字典形式，例如：[{'field': 'name', 'unique': True}]
        :return: 操作结果字典
        """
        try:
            if collection_name in self.db.list_collection_names():
                return {"success": False, "message": f"Collection '{collection_name}' already exists."}

            collection = self.db.create_collection(collection_name)

            # 创建索引（如果有）
            if indexes:
                for index in indexes:
                    field = index.get("field")
                    unique = index.get("unique", False)
                    if field:
                        collection.create_index([(field, 1)], unique=unique)

            return {"success": True, "message": f"Collection '{collection_name}' created successfully."}
        except CollectionInvalid as e:
            return {"success": False, "message": str(e)}
        except Exception as e:
            return {"success": False, "message": f"An error occurred: {str(e)}"}

    def close_connection(self):
        """关闭 MongoDB 连接"""
        self.client.close()

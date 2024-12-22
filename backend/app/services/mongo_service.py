from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from backend.app.config import Config


class MongoDatabaseManager:
    _connection = None

    @classmethod
    def get_connection(cls):
        """
        获取全局 MongoDB 数据库连接。如果不存在，则创建一个新连接。
        """
        if cls._connection is None:
            cls._connection = MongoClient(Config.MONGO_URI)
        return cls._connection[Config.MONGO_DB_NAME]

    @classmethod
    def close_connection(cls):
        """
        关闭全局 MongoDB 数据库连接。
        """
        if cls._connection:
            cls._connection.close()
            cls._connection = None

def create_collection(collection_name: str, indexes: list = None):
    """
    创建集合，并可选配置索引。
    """
    try:
        db = MongoDatabaseManager.get_connection()
        if collection_name in db.list_collection_names():
            return {"status": "error", "message": f"Collection '{collection_name}' already exists."}

        collection = db.create_collection(collection_name)

        # 创建索引
        if indexes:
            for index in indexes:
                field = index.get("field")
                unique = index.get("unique", False)
                if field:
                    collection.create_index([(field, 1)], unique=unique)

        return {"status": "success", "message": f"Collection '{collection_name}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def insert_data(collection_name: str, data: list):
    try:
        db = MongoDatabaseManager.get_connection()
        collection = db[collection_name]

        # 确保 data 是列表
        if not isinstance(data, list):
            data = [data]

        result = collection.insert_many(data)

        if not result.inserted_ids:
            raise ValueError("No documents were inserted.")

        return {
            "status": "success",
            "message": "Data inserted successfully.",
            "inserted_ids": [str(_id) for _id in result.inserted_ids],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_data(collection_name: str, filter_query: dict, update_values: dict, multi: bool = False):
    """
    更新集合中的数据。

    :param collection_name: 集合名称
    :param filter_query: 筛选条件
    :param update_values: 更新字段和值
    :param multi: 是否更新多条数据（默认 False）
    :return: 操作结果字典
    """
    try:
        db = MongoDatabaseManager.get_connection()
        collection = db[collection_name]

        # 构造更新操作
        update_operation = {"$set": update_values}

        if multi:
            result = collection.update_many(filter_query, update_operation)
        else:
            result = collection.update_one(filter_query, update_operation)

        return {
            "status": "success",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "message": "Update operation completed."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def delete_data(collection_name: str, filter_query: dict, multi: bool = False):
    """
    删除集合中的数据。

    :param collection_name: 集合名称
    :param filter_query: 筛选条件
    :param multi: 是否删除多条数据（默认 False）
    :return: 操作结果字典
    """
    try:
        db = MongoDatabaseManager.get_connection()
        collection = db[collection_name]

        # 根据 multi 参数执行删除操作
        if multi:
            result = collection.delete_many(filter_query)
        else:
            result = collection.delete_one(filter_query)

        return {
            "status": "success",
            "message": "Delete operation completed.",
            "deleted_count": result.deleted_count,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}



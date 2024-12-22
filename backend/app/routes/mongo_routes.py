import logging
import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.app.services.mongo_service import create_collection, insert_data
from typing import List

# 初始化日志记录器
logger = logging.getLogger(__name__)
router = APIRouter()

# 定义请求体模型
class CreateCollectionRequest(BaseModel):
    collection_name: str = Field(..., min_length=1, max_length=100, description="集合名称")
    indexes: List[dict] = Field(default=[], description="索引配置列表")

class InsertDataRequest(BaseModel):
    collection_name: str = Field(..., min_length=1, max_length=100, description="集合名称")
    data: List[dict] = Field(..., description="待插入的数据")

# 定义响应模型
class InsertDataResponse(BaseModel):
    message: str
    inserted_ids: List[str]

@router.post("/create-collection")
def create_collection_endpoint(request: CreateCollectionRequest):
    """
    创建集合的 API 端点。
    """
    try:
        result = create_collection(request.collection_name, request.indexes)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return {"message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert-data", response_model=InsertDataResponse)
def insert_data_endpoint(request: InsertDataRequest):
    """
    插入数据的 API 端点。
    """
    try:
        result = insert_data(request.collection_name, request.data)
        if result["status"] == "error":
            logger.error(f"Insert data error: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        return {
            "message": result["message"],
            "inserted_ids": result["inserted_ids"],
        }
    except Exception as e:
        # 捕获完整的异常信息
        error_message = f"Unhandled exception: {str(e)}"
        error_traceback = traceback.format_exc()
        logger.error(f"{error_message}\n{error_traceback}")
        raise HTTPException(
            status_code=500,
            detail=f"{error_message} | Traceback: {error_traceback}",
        )
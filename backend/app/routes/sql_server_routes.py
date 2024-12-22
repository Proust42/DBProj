# backend/app/routes/sql_server_routes.py
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from ..services.sql_server_service import create_table, insert_data, delete_data, update_data, delete_table, join_tables

router = APIRouter()

# 定义请求体模型
class InsertDataRequest(BaseModel):
    table_name: str
    columns: list
    values: list

@router.post("/create_table")
def create_table_endpoint(table_name: str, table_query: str):
    """
    创建表的 API 端点
    - 参数:
        - table_name: 表名（仅用于描述）
        - table_query: 完整的 CREATE TABLE SQL 语句
    """
    result = create_table(table_query)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": f"Table '{table_name}' created successfully."}


@router.post("/insert_data")
def insert_data_endpoint(request: InsertDataRequest):
    """
    插入数据的 API 端点。
    :param request: 包含表名、字段名列表和字段值列表的请求体
    """
    try:
        # 解包请求数据
        result = insert_data(request.table_name, request.columns, request.values)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return {"message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_data")
def delete_data_endpoint(table_name: str, condition: str):
    """
    删除指定表中符合条件的数据。
    - 参数:
        - table_name: 表名
        - condition: 删除条件
    """
    result = delete_data(table_name, condition)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": result["message"]}

@router.put("/update_data")
def update_data_endpoint(
    table_name: str,
    condition: str,
    updates: list[str] = Form(...),
):
    """
    更新数据的 API 端点
    """
    result = update_data(table_name, condition, updates)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result



@router.delete("/delete_table")
def delete_table_endpoint(table_name: str):
    """
    删除数据表的 API 端点。
    """
    result = delete_table(table_name)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/join_tables")
def join_tables_endpoint(query: str):
    """
    跨表 JOIN 查询的 API 端点。
    :param query: 完整的 SQL 查询语句（如 JOIN 操作）。
    """
    result = join_tables(query)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result
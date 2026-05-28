# src/routes/todo.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
# 引入你在 auth.py 中写好的 Token 验证器
from src.middleware.auth import verify_token 
from src.controllers import todo as todo_controller

# 创建路由组
router = APIRouter(prefix="/todos", tags=["Todo"])

# 定义前端传过来的数据格式
class TodoCreate(BaseModel):
    title: str

@router.get("/")
async def get_todos(current_user: dict = Depends(verify_token)):
    # Depends(verify_token) 会在执行代码前自动验证请求头里的 Token
    # 如果验证通过，current_user 就会拿到你解析出来的 {"user_id": ..., "username": ...}
    return todo_controller.get_user_todos(current_user["user_id"])

@router.post("/")
async def add_todo(todo_in: TodoCreate, current_user: dict = Depends(verify_token)):
    return todo_controller.create_todo(current_user["user_id"], todo_in.title)
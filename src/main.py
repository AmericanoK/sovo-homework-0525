from fastapi import FastAPI
import uvicorn
from src.routes.auth import router as auth_router
from src.routes.todo import router as todo_router  # 👈 新增：导入待办事项路由
# 导入你 models.py 里的 db 实例
from src.models import db 

app = FastAPI(title="SOVO Homework API")

# 【核心修复】加入 Peewee 数据库连接的中间件
@app.middleware("http")
async def db_session_middleware(request, call_next):
    # 1. 在请求到达路由前，如果连接关闭了，则打开它
    if db.is_closed():
        db.connect()
    try:
        response = await call_next(request)
        return response
    finally:
        # 2. 请求结束后，无论成功失败，都关闭连接释放资源
        if not db.is_closed():
            db.close()

# 挂载认证路由
app.include_router(auth_router)
# 挂载待办事项路由
app.include_router(todo_router) # 👈 新增：将待办事项路由挂载到服务中

@app.get("/")
async def root():
    return {"message": "SOVO 后端服务已成功启动！"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
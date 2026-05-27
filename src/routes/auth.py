from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import datetime

# ==================== 引入核心依赖 ====================
# 1. 导入你真实的 Peewee 数据库模型
from src.models import User 
# 2. 导入中间件的校验逻辑和密钥
from src.middleware.auth import JWT_SECRET, ALGORITHM, verify_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# 初始化密码加密上下文（使用 bcrypt 算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定义前端传过来的数据格式
class UserAuthSchema(BaseModel):
    username: str
    password: str

# ==================== 1. 注册接口 ====================
@router.post("/register")
async def register(data: UserAuthSchema):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")
    
    try:
        # 使用 Peewee 去 MySQL 查用户名是否已存在
        user_exists = User.select().where(User.username == data.username).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 对密码进行 Hash 加密
        hashed_password = pwd_context.hash(data.password)
        
        # 将真实数据存入 MySQL 数据库
        User.create(
            username=data.username, 
            password_hash=hashed_password
        )
        
        return {"message": "注册成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库错误: {str(e)}")

# ==================== 2. 登录接口 ====================
@router.post("/login")
async def login(data: UserAuthSchema):
    try:
        # 使用 Peewee 根据用户名查找用户
        user = User.select().where(User.username == data.username).first()
        if not user:
            raise HTTPException(status_code=401, detail="用户名或密码错误")
            
        # 比对前端输入的明文密码与数据库中的 Hash 值
        if not pwd_context.verify(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        # 登录成功，生成 JWT Token（设置 2 小时过期，强制使用中国标准时间 UTC+8）
        china_tz = datetime.timezone(datetime.timedelta(hours=8))
        expire_time = datetime.datetime.now(china_tz) + datetime.timedelta(hours=2)
        
        token_payload = {
            "user_id": user.id,          # 真实的数据库自增 ID
            "username": user.username,    # 真实的用户名
            "exp": expire_time            # 中国时间的过期时间戳
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm=ALGORITHM)
        
        return {"message": "登录成功", "token": token}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

# ==================== 3. 受保护路由 ====================
@router.get("/me")
async def get_me(current_user: dict = Depends(verify_token)):
    # 只有通过 verify_token 校验的请求才能走到这里
    return {
        "message": "获取成功，你已进入受保护路由",
        "user": current_user
    }
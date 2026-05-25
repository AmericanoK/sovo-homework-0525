from peewee import MySQLDatabase, Model, CharField, DateTimeField, ForeignKeyField, BooleanField
import datetime

# 1. 初始化数据库连接
db = MySQLDatabase(
    'sovowork',             
    host='127.0.0.1',       
    port=3306,              
    user='root',           
    password='123456789', 
    charset='utf8mb4'       
)

# 2. 创建基础模型类
class BaseModel(Model):
    class Meta:
        database = db

# 3. 映射用户表 (User)
class User(BaseModel):
    username = CharField(max_length=50, unique=True)
    password_hash = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'user'

# 4. 映射待办事项表 (Todo)
class Todo(BaseModel):
    user = ForeignKeyField(User, backref='todos', on_delete='CASCADE', column_name='user_id')
    title = CharField(max_length=255)
    is_completed = BooleanField(default=False)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'todo'
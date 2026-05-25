from models import db, User

def test_connection():
    try:
        db.connect()
        print("数据库连接成功！")
        user_count = User.select().count()
        print(f"📊 当前数据库中共有 {user_count} 个用户。")
        
    except Exception as e:
        print("数据库连接失败")
    finally:
        if not db.is_closed():
            db.close()
if __name__ == '__main__':
    test_connection()
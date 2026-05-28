# src/controllers/todo.py
from src.models import Todo

def get_user_todos(user_id: int):
    todos = Todo.select().where(Todo.user == user_id)
    return [{"id": t.id, "title": t.title, "is_completed": t.is_completed} for t in todos]

def create_todo(user_id: int, title: str):
    """为指定用户创建一条新待办"""
    new_todo = Todo.create(user=user_id, title=title)
    return {"id": new_todo.id, "title": new_todo.title, "is_completed": new_todo.is_completed}
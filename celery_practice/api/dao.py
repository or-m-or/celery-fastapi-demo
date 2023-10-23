# (Data Access Object) - 데이터베이스와 상호 작용:

from api.dto import User, CreateUser

# 가상 데이터베이스 대신 리스트를 사용.
db = []
db_id = 0

def get_users():
    return db

def create_user(user: CreateUser):
    global db_id
    db_id += 1
    # user_data = User(id=db_id, **user)
    user_data = user
    db.append(user_data)
    return user_data

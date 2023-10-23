from app import celery_app
from api.dto import CreateUser
from api.svc import add_user
from api.dto import User

@celery_app.task
def test(x, y):
    import time
    time.sleep(3)
    return x + y

# Celery 작업을 생성하는 함수
@celery_app.task
def create_user_celery_task(name, password):

    user = to_dict(name, password)
    # user = User(name=name, password=password)
    # user = CreateUser(name=name, password=password)
    return add_user(user)

def to_dict(name, password):
    return {
        "name":name,
        "password":password
    }
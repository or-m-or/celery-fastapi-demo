# (Service) - 비즈니스 로직 처리:

from api.dao import get_users, create_user
from api.dto import CreateUser

def get_user_list():
    return get_users()

def add_user(user: CreateUser):
    return create_user(user)

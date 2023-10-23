# (Data Transfer Object) - 데이터 모델 정의:
from typing import Annotated
from fastapi import Depends, Form, Path
from pydantic import BaseModel

class User(BaseModel):
    name: Annotated[str, Form(description="이름")]
    password: Annotated[str, Form(description="비밀번호")]

class CreateUser(User):
    ...

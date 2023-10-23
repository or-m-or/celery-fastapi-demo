# (Controller) - FastAPI 라우팅 및 핸들러:
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from api.svc import get_user_list, add_user
from api.dto import User, CreateUser
from api.dto import User as ApiUser, CreateUser as ApiCreateUser
from celery import Celery
from celery.result import AsyncResult
from worker import test, create_user_celery_task
from app import celery_app
import json

ns = APIRouter(
    prefix="/celerytest",
)

"""
document참조 original 버전 : task를 별도 함수로 선언하여 라우터에서 바로 호출


[ 참고 ]
-> task 데코레이션이 붙은 함수를 실행할 때 사용가능한 메소드
1. apply_async : 해당 함수를 비동기적으로 실행
              결과를 얻으려면 작업의 반환 값을 따로 가져와야 함
2. delay : 작업 함수를 호출하는 데 편리하게 사용가능
        작업을 대기열에 넣고 결과를 반환하지 않음 -> 결과를 가져올 필요가 없는 경우 사용
"""
@ns.get(
    "/work",
    summary="셀러리-radis 분산작업 테스트",
    description="task message -> 메세지 브로커(task) -> 셀러리 Worker -> Result Backend"    
)
async def work(task_id: str, input_a: int, input_b: int):
    test.apply_async([input_a, input_b], task_id=task_id)
    return {"message": "Celery 작업이 시작되었습니다.", "task_id": task_id}


@ns.get(
    "/work_result",
    summary="셀러리-radis 작업결과 확인하기",
    description="Result Backend에 존재하는 결과 값 가져오기",
)
async def work_result(task_id: str):
    result = test.AsyncResult(task_id)
    if result.state == 'SUCCESS':
        return {"message": "작업이 완료되었습니다.", "result": result.info}
    elif result.state == 'PENDING':
        return {"message": "작업이 진행 중입니다."}
    else:
        return {"message": "작업이 실패했습니다.", "result": result.info}



"""
유레카쳇 아키텍처 참조 버전 
""" 
@ns.get(
    "/users/", 
    summary="사용자 조회",
    response_model=list[User],
)
def read_users():
    return get_user_list()


@ns.post(
    "/users/",
    summary="그냥 사용자 생성",
    response_model=User
)
def create_user(user: Annotated[CreateUser, Depends()]):
    return add_user(user)


# Celery 작업을 생성하는 FastAPI 엔드포인트 추가
@ns.post(
    "/create_user_celery",
    summary="Celery를 사용하여 사용자 생성",
    response_model=User,
)
async def create_user_celery(name: str, password: str):    
    # Celery 작업을 비동기로 실행
    result = create_user_celery_task.apply_async(args=[name, password])
    # test.apply_async([input_a, input_b], task_id=task_id)
    # Celery 작업이 완료되면 결과를 가져와서 응답 구성
    return {"message": "Celery 작업이 시작되었습니다.", "task_id": result.id}




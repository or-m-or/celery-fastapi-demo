# celery-fastapi-demo
fastapi에 celery를 적용시키기 위한 데모버전 앱 (Redis 사용) 


## celery-fastapi 데모버전 테스트 (with Redis)
---



1. 샐러리 서버 실행

         celery -A app.celery_app  worker --loglevel=info




2. 샐러리 워커 현황 조회

         celery -A app.celery_app flower --port=5555




3. fastapi app 실행 

         uvicorn main:app --reload

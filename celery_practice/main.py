from fastapi import FastAPI

from api.ctl import ns


app = FastAPI()


app.include_router(ns)
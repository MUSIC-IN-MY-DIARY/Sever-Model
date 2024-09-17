from fastapi import APIRouter
# default Settings

from .question_schemas import *
from models.Models import *
from config.InsertData import *
# Modules

question_router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)

# 기본 프레픽스, /question 이라는 엔드포인트로 띄워자게    됨

@question_router.post("/", response_model=QuestionSchema)
async def read_root():
    return "hello"




import os

from fastapi import APIRouter, HTTPException
# default Settings

from .question_schemas import QuestionSchema,AnswerSchema


# Modules

test_router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)

@test_router.get("/question")
async def get_question():
    return os.getenv("OPENAI_API_KEY")

from http.client import HTTPException

from fastapi import APIRouter, HTTPException
# default Settings

from .question_schemas import QuestionSchema,AnswerSchema
from model.Embedding_Chatbot import Embedding_Chatbot

# Modules

question_router = APIRouter(
    prefix="/recommend",
    tags=["recommend"],
    responses={404: {"description": "Not found"}},
)

# 기본 프레픽스, /question 이라는 엔드포인트로 띄워자게    됨

@question_router.post("/", response_model=AnswerSchema)
async def question_models(recommend: QuestionSchema):
    chatbot = Embedding_Chatbot()
    try:
        answer_text = chatbot.answer_question(recommend.recommend)
        return AnswerSchema(answer=answer_text)
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))





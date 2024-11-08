from http.client import HTTPException

from fastapi import APIRouter, HTTPException
# default Settings

from .generate_schemas import GenerateSchema, ReturnAnswer
from model.Embedding_Chatbot import Embedding_Chatbot

generate_router = APIRouter(
    prefix="/generate",
    tags=["generate"],
    responses={404: {"description": "Not found"}},
)

@generate_router.post("/", response_model=ReturnAnswer)
async def generate_model(generate : GenerateSchema):
    chat = Embedding_Chatbot()
    try:
        generate_text = chat.generate_answer(generate.generate)
        return ReturnAnswer(diaryContent = generate_text)
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))


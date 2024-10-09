from pydantic import BaseModel

class QuestionSchema(BaseModel):
    question: str

class AnswerSchema(BaseModel):
    answer: str
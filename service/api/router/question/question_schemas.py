from pydantic import BaseModel

class QuestionSchema(BaseModel):
    diaryContent : str

class AnswerSchema(BaseModel):
    answer: str
from pydantic import BaseModel

class QuestionSchema(BaseModel):
    recommend : str

class AnswerSchema(BaseModel):
    diaryContent: str
from pydantic import BaseModel

class GenerateSchema(BaseModel):
    diaryContent : str

class ReturnAnswer(BaseModel):
    answer : str


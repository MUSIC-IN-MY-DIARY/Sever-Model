from pydantic import BaseModel

class GenerateSchema(BaseModel):
    generate : str

class ReturnAnswer(BaseModel):
    answer : str


import openai
from openai import OpenAI
# openai API

from .Authentication import Authentication
# Modules

from typing import List, Dict
class Embedding_Chatbot:
    def __init__(self: str) -> str:
        self.client = OpenAI(
            api_key=Authentication().get_token()
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client.embeddings.create
        # 기초 model parts 생성
    def get_embedding(self, text: str) -> Dict[str, List[float]]:
        text = text.replace('\n', ' ')
        return self.embedding_model(
            input = [text],
            model = model
        ).data[0].embedding
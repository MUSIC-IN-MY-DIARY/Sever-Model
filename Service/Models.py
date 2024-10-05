from openai import OpenAI
# openai API

from service.Authentication import Authentication
from .RedisManager import RedisVectorStore
# Modules

from typing import List, Dict

class Embedding_Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=Authentication().get_token()
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client \
            .embeddings\
            .create
        self.vector_store = RedisVectorStore()

        # 기초 model parts 생성
    def get_embedding(self, text: str) -> List[float]:
        text = text.replace('\n', ' ')
        return self.embedding_model(
            input = [text],
            model = model
        ).data[0].embedding

    def create_context(self, question: str, max_len: int = 1800) -> str:
        simliar_docs = self.vector_store \
            .search_similar_artist(question, top_k= 5)
        if not simliar_docs:
            return ""
        cur_len = 0
        context_parts = []
        for doc in simliar_docs:
            content = doc['content']
            additional_length = len(content.split()) + 4
            if cur_len + additional_length > max_len :
                break
            context_parts.append(content)
            cur_len += additional_length
        return "\n".join(context_parts)

    def answer_question(self, question: str, max_len: int=1800) -> str:
        context = self.create_context(question, max_len=max_len)
        if not context:
            return "I don't know"

        try:
            response = self.client \
                .chat\
                .completions \
                .create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Answer the question based on the context below, try to explain anyway but if the question can't be answered based on the context, say \"I don't know\"\n\n",

                    },
                    {
                        "role": "user",
                        "content": f"Context: {context}\n\n---\n\nQuestion: {question}, 한국어로 번역해서 대답해"
                    },
                ],
                temperature=0,
            )
            return response.choices[0] \
                .message \
                .content.strip()
        except Exception as e:
            print(e)
            return "I don't know"
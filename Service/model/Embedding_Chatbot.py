from openai import OpenAI
# openai API

from ..config.Authentication import Authentication
from data.redis_data.RedisManager import RedisVectorStore
# Modules

from typing import List


class Embedding_Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=Authentication().get_token()
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client\
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
        simliar_docs = self.vector_store\
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

    def answer_question(self, question: str, max_len: int = 1800) -> str:
        context = self.create_context(question, max_len=max_len)
        system_message = """
        당신은 음악 전문가이자 작사가입니다. 사용자 질문에 따라 적절한 답변을 제공해야 합니다.
        - 음악 및 특정 데이터에 대한 정보 조회 요청 시 데이터베이스의 정보를 기반으로 질문에 대한 정확한 답변만 제공합니다(제공된 데이터 종류: 이름, 본명, 생년월일, 데뷔, 그룹, 히트곡, 특징)        
        - 노래 가사 생성 요청 시, 위에서 제공해준 데이터를 기반으로 창의적인 가사를 생성해줍니다.(무조건 생성이라는 질문에만 답변을 줘야함)        
        """

        if context:
            message = f"질문: '{question}'\n\n관련 정보:\n{context}\n\n위의 정보를 참고하여 답변해 주세요."
        else:
            message = f"질문: '{question}'\n\n위 질문에 답변해 주세요."

        try:
            response = self.client\
                .chat\
                .completions\
                .create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_message,
                    },
                    {
                        "role": "user",
                        "content": message
                    },
                ],
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"응답 생성 중 오류 발생: {e}")
            return "죄송합니다. 답변을 생성할 수 없습니다."
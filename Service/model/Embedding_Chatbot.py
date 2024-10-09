from openai import OpenAI
# openai API

from config.Authentication import Authentication
# Modules

from redis import Redis
from redis.commands.search.query import Query
import numpy as np
from typing import List

# packages

class Embedding_Chatbot:
    def __init__(self, index_name='artist_vector_store'):
        self.client = OpenAI(
            api_key=Authentication().get_token()
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client\
            .embeddings\
            .create

        # VectorStore
        self.redis_conn = Redis()
        self.index_name = index_name

        # 기초 model parts 생성
    def get_embedding(self, text: str) -> List[float]:
        text = text.replace('\n', ' ')
        return self.embedding_model(
            input = [text],
            model = model
        ).data[0].embedding

    def search_similar_artist(self, query_text: str, top_k: int = 3):
        """
        입력 테스트와 유사한 아티스트 벡터를 검색
        :param query_text:
        :param top_k:
        :return:
        """

        query_response = self.client.embeddings.create(
            input=[query_text],
            model='text-embedding-3-small'
        )
        query_embedding = query_response.data[0].embedding

        np_query_embedding = np.array(query_embedding, dtype=np.float32).tobytes()

        query = f"*=>[KNN {top_k} @embedding $vec_param AS dist]"
        params_dict = {
            "vec_param" : np_query_embedding,
        }
        try:
            # Query 객체 생성 및 다이얼렉트 설정
            q = Query(query) \
                .return_fields("content","이름", "그룹", "특징", "dist") \
                .sort_by("dist") \
                .paging(0, top_k) \
                .dialect(2)  # 다이얼렉트 2로 설정

            results = self.redis_conn.ft(self.index_name).search(q, query_params=params_dict)
            return results.docs  # 검색된 문서 리스트 반환
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def create_context(self, question: str, max_len: int = 1800) -> str:
        simliar_docs = self.search_similar_artist(question, top_k= 5)
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






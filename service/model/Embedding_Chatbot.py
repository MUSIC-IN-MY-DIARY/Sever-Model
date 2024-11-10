from openai import OpenAI
# openai API

import os
from redis import Redis
from redis.commands.search.query import Query
import numpy as np
from typing import List, Dict




# packages

class Embedding_Chatbot:
    def __init__(self, index_name='artist_vector_store'):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client\
            .embeddings\
            .create

        # VectorStore
        self.redis_conn = Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
        )
        self.index_name = index_name

        # 기초 model parts 생성
    def get_embedding(self, text: str) -> List[float]:
        text = text.replace('\n', ' ')
        return self.embedding_model(
            input = [text],
            model = 'text-embedding-3-small'
        ).data[0].embedding

    def search_similar_artist(self, query_text: str, top_k: int = 3):
        """
        입력 테스트와 유사한 아티스트 벡터를 검색
        :param query_text:
        :param top_k:
        :return:
        """

        query_embedding = self.get_embedding(query_text) # 기존 코드 간소화
        np_query_embedding = np.array(query_embedding, dtype=np.float32).tobytes() # 리턴 값을 위해 바이트로 변환

        query = f"*=>[KNN {top_k} @embedding $embedding AS dist]" # KNN 기법으로, 임베딩 벡터필드란 안에서 일리야스로 dist /
        params_dict = {
            "embedding" : np_query_embedding,
        }
        try:
            # Query 객체 생성 및 다이얼렉트 설정
            q = Query(query) \
                .return_fields("content", "title", "artist", "album", "genre", "release_date", "lyrics", "image", "song_id", "artist_id", "album_id", "sys_date") \
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


    def answer_question(self, question: str, max_len: int = 1800) -> List[Dict]:
        context = self.create_context(question, max_len=max_len)
        system_message = """
        당신은 음악 전문가이자 작사가입니다. 
        
        사용자 요청이 노래 정보, 비슷한 장르를 추천해 달라는 질문이 왔을 때 노래 정보를 제공해주세요 다음 항목을 포함해야 합니다:
        - title
        - artist
        - genre
        - song_id
        
        예시 JSON 형식:
        [
            {
                "song_title": "APT.",
                "artist": "로제 (ROSÉ)",
                "genre": "댄스",
                "song_id": "38120327"
            },
            {
                "song_title" : "UP (KARINA Solo)",
                "artist": "aespa",
                "genre": "댄스",
                "song_id": "38077932"
            },
            {
                "song_title" : "Supernova",
                "artist": "aespa",
                "genre": "댄스",
                "song_id": "37524037"
            }
        ]
        상기 양식에 맞게 노래 정보에 대해서 물어볼 때 결과를 JSON 형태로 제공해주세요 

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

    def generate_answer(self, question: str, max_len: int = 2800) -> str:
        context = self.create_context(question, max_len=max_len)
        system_message = """
        당신은 음악 전문가이자 작사가입니다. 
                 
        사용자 요청이 가사 생성일 때 하기 형식에 맞게 노래가사를 생성해주세요. 출력 형식은 순수 문자열 형태로 제공해야 합니다.
        예시 문자열 형식:
        걸어가다가 몇 번이나 멈춰서, 네 모습이 없는 거리 위에서 혼자 남아 있다. 
        그때, 함께였던 모든 순간들이 가슴을 파고드는 것 같아. 
        빈자리가 자꾸만 커져, 돌아갈 수 없는 길 위에 서 있는 우리. 사랑이 이유라면 아프게 이별하는 건, 정말이지 할 수 없는 일 같아. 
        더는 널 떠날 수 없는 나, 돌아갈 길은 멀지만 끝내 멈추지 못할 것 같아.
        
        상기 양식에 맞게 사용자가 얘기하는 조건에 맞는 노래 가사를 순수 문자열 형태로 제공해주세요.
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






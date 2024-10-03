from openai import OpenAI
import numpy as np
from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition
from redis.exceptions import ResponseError

# KeyChain Settings
from .Authentication import Authentication

class RedisVectorStore:
    def __init__(self, index_name='artist_vector_store'):
        self.index_name = index_name
        self.redis_conn = Redis(host='localhost', port=6379, db=0)

        self.client = OpenAI(
            api_key=Authentication().get_token()
        )

    def create_vector_index(self):
        """RediSearch 인덱스 생성"""
        try:
            # 인덱스가 이미 존재하는지 확인
            self.redis_conn.ft(self.index_name).info()
            print(f"Index '{self.index_name}' already exists.")
        except ResponseError as e:
            # 'Index does not exist' 에러가 발생하면 인덱스 생성
            if "Index does not exist" in str(e) or "Unknown index name" in str(e):
                print(f"Index '{self.index_name}' not found, creating a new one...")
                schema = (
                    TextField("이름", weight=1.0),      # 숫자형 `WEIGHT` 값으로 설정
                    TextField("본명", weight=0.8),
                    TextField("생년월일", weight=0.5),
                    TextField("데뷔", weight=0.6),
                    TextField("그룹", weight=1.0),
                    TextField("히트곡", weight=0.9),
                    TextField("특징", weight=1.2),
                    VectorField("embedding",
                                "FLAT",
                                {"TYPE": "FLOAT32",
                                 "DIM": 1536,
                                 "DISTANCE_METRIC": "COSINE"})
                )
                # 인덱스 생성
                self.redis_conn.ft(self.index_name).create_index(
                    schema,
                    definition=IndexDefinition(prefix=[f"{self.index_name}:"])
                )
                print(f"Created index: {self.index_name}")
            else:
                print(f"An error occurred: {e}")
                raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    def insert_data(self, artist_id: str, artist_info: dict):
        """
        아티스트 데이터를 임베딩으로 변환하여 Redis에 삽입
        :param self:
        :param artist_id:
        :param artist_info:
        :return:
        """
        content = f"{artist_info['이름']} ({artist_info['본명']}), {artist_info['그룹']}, 생년월일: {artist_info['생년월일']}, 히트곡: {', '.join(artist_info['히트곡'])}, 특징: {artist_info['특징']}"

        # Embbeding 생성
        response = self.client.embeddings.create(
            input=[content],
            model='text-embedding-3-small'
        )
        embedding = response.data[0].embedding

        np_embedding = np.array(embedding, dtype=np.float32).tobytes()
        self.redis_conn.hset(f"{self.index_name}:{artist_id}", mapping={
            "이름": artist_info['이름'],
            "본명": artist_info['본명'],
            "생년월일": artist_info['생년월일'],
            "그룹": artist_info['그룹'],
            "히트곡": ', '.join(artist_info['히트곡']),
            "특징": artist_info['특징'],
            "content": content,  # 전체 내용을 content 필드에 저장
            "embedding": np_embedding  # 임베딩 벡터 저장
        })
        print(f"Inserted data for {artist_info['이름']}")

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

        results = self.redis_conn.ft(self.index_name).search(query, query_params=params_dict)
        for doc in results.docs:
            print(f"Document ID: {doc.id}, 이름: {doc['이름']}, 그룹: {doc['그룹']}, 특징: {doc['특징']}, Distance: {doc.dist}")



# Redis Modules
from redis import Redis
from redis.commands.search.field import TextField, VectorField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition
from redis.exceptions import ResponseError
import numpy as np
from openai import OpenAI


from datetime import datetime

import os


class RedisVectorStore:
    def __init__(self, index_name='artist_vector_store'):
        redis_host = os.getenv('REDIS_HOST')
        redis_port = int(os.getenv('REDIS_PORT'))
        redis_password = os.getenv('REDIS_PASSWORD')

        self.index_name = index_name
        self.redis_conn = Redis(host=redis_host, port=redis_port, db=0, password=redis_password)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
                    TextField("title", weight=5.0),      # 곡 제목 필드
                    TextField("artist", weight=3.0),     # 아티스트 이름 필드
                    TextField("album", weight=2.0),      # 앨범 이름 필드
                    TextField("genre", weight=1.0),      # 장르 필드
                    TextField("release_date"),        # 발매일 필드
                    TextField("lyrics", weight=1.0),     # 가사 필드 (저작권 고려 필요)
                    TextField("image"),                  # 이미지 URL 필드
                    TextField("song_id"),                # 곡 ID 필드
                    TextField("artist_id"),              # 아티스트 ID 필드
                    TextField("album_id"),               # 앨범 ID 필드
                    TextField("sys_date"),            # 아티스트 데뷔년도 필드 추가
                    VectorField("embedding",             # 임베딩 필드
                                "FLAT",  # 또는 "HNSW" (검색 성능에 따라 선택)
                                {
                                    "TYPE": "FLOAT32",
                                    "DIM": 1536,
                                    "DISTANCE_METRIC": "COSINE"
                                })
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

    def insert_data(self, id: str, data: dict, data_type: str = 'song'):
        """
        데이터를 임베딩으로 변환하여 Redis에 삽입
        :param id: 곡 ID 또는 아티스트 ID
        :param data: 곡 정보 또는 아티스트 정보 딕셔너리
        :param data_type: 'song' 또는 'artist'로 데이터 유형 지정
        :return: None
        """
        # 로깅으로 데이터 형태와 ID 확인
        if data_type == 'song':
            # 곡 데이터 처리
            print(f"Song details: {data['song_detail']}")  # sys_date 값 확인
            sys_date = data['song_detail']['sys_date']
            lyrics = data['song_detail']['lyric']

            content = f"{data['title']} by {data['artist']}, from album: {data['album']}, genre: {data['song_detail']['genre']}, released on: {sys_date} lyrics : {lyrics}, song_id: {data['song_id']}"

            # Embedding 생성
            response = self.client.embeddings.create(input=[content], model='text-embedding-3-small')
            embedding = response.data[0].embedding
            np_embedding = np.array(embedding, dtype=np.float32).tobytes()

            # Redis에 데이터 저장
            self.redis_conn.hset(f"{self.index_name}:{id}", mapping={
                "title": data['title'],
                "artist": data['artist'],
                "album": data['album'],
                "genre": data['song_detail']['genre'],
                "lyrics": data['song_detail']['lyric'],
                "image": data['image'],
                "song_id": data['song_id'],
                "artist_id": data['song_detail']['artist_id'],
                "album_id": data['song_detail']['album_id'],
                "sys_date": sys_date,
                "content": content,
                "embedding": np_embedding
            })
            print(f"Inserted data for song '{data['title']}'")
            print(f"Inserting data for ID: {id}, Data type: {type(data)}")
            print(f"Data content: {data}")


        elif data_type == 'artist':
            # 아티스트 데이터 처리 (title 없음)
            content = f"Artist: {data['art_info']}, Debut: {data['debut_date']}"
            # Redis에 아티스트 데이터 저장
            self.redis_conn.hset(f"{self.index_name}:{id}", mapping={
                "debut_date": data.get('debut_date', ''),
                "art_info": ', '.join(data.get('art_info', [])),
                "awards": ', '.join(data.get('awards', [])),
                "content": content  # 아티스트 요약 정보
            })
            print(f"Inserted data for artist '{id}'")
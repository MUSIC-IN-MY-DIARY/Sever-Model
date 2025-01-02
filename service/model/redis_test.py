from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition
from redis.exceptions import ResponseError
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os

# .env 파일 로드
load_dotenv()

def test_data_insertion():
    redis_conn = Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    
    # 테스트용 곡 데이터
    test_song_data = {
        'title': 'Test Song',
        'artist': 'Test Artist',
        'album': 'Test Album',
        'song_id': 'test_song_001',
        'image': 'http://test.com/image.jpg',
        'song_detail': {
            'genre': 'K-pop',
            'sys_date': '2024-03-21',
            'lyric': 'Test lyrics...',
            'artist_id': 'test_artist_001',
            'album_id': 'test_album_001'
        }
    }
    
    # 테스트용 아티스트 데이터
    test_artist_data = {
        'art_info': ['Test artist biography'],
        'debut_date': '2020-01-01',
        'awards': ['Best New Artist 2020', 'Song of the Year 2021']
    }
    
    try:
        # 1. 곡 데이터 저장 테스트
        print("\nTesting song data insertion...")
        redis_conn.hset(
            f"artist_vector_store:song:test_song_001",
            mapping={
                "title": test_song_data['title'],
                "artist": test_song_data['artist'],
                "album": test_song_data['album'],
                "genre": test_song_data['song_detail']['genre'],
                "lyrics": test_song_data['song_detail']['lyric'],
                "image": test_song_data['image'],
                "song_id": test_song_data['song_id'],
                "artist_id": test_song_data['song_detail']['artist_id'],
                "album_id": test_song_data['song_detail']['album_id'],
                "sys_date": test_song_data['song_detail']['sys_date']
            }
        )
        print("Song data inserted successfully!")
        
        # 2. 아티스트 데이터 저장 테스트
        print("\nTesting artist data insertion...")
        redis_conn.hset(
            f"artist_vector_store:artist:test_artist_001",
            mapping={
                "debut_date": test_artist_data['debut_date'],
                "art_info": ', '.join(test_artist_data['art_info']),
                "awards": ', '.join(test_artist_data['awards'])
            }
        )
        print("Artist data inserted successfully!")
        
        # 3. 저장된 데이터 확인
        print("\nVerifying stored data...")
        song_data = redis_conn.hgetall("artist_vector_store:song:test_song_001")
        artist_data = redis_conn.hgetall("artist_vector_store:artist:test_artist_001")
        
        print("\nStored song data:")
        for key, value in song_data.items():
            print(f"- {key}: {value}")
            
        print("\nStored artist data:")
        for key, value in artist_data.items():
            print(f"- {key}: {value}")
        
    except Exception as e:
        print(f"Error during data insertion: {e}")

def test_embedding_creation():
    # OpenAI 클라이언트 초기화
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # decode_responses=True 제거
    redis_conn = Redis(
        host='localhost',
        port=6379
    )
    
    # 테스트용 텍스트 데이터
    test_text = "Test Song by Test Artist, from album: Test Album, genre: K-pop, released on: 2024-03-21 lyrics: Test lyrics..."
    
    try:
        # 임베딩 생성
        print("\nGenerating embedding...")
        response = client.embeddings.create(
            input=[test_text],
            model='text-embedding-3-small'
        )
        embedding = response.data[0].embedding
        np_embedding = np.array(embedding, dtype=np.float32).tobytes()
        
        # Redis에 임베딩 저장
        print("\nSaving embedding to Redis...")
        redis_conn.hset(
            "artist_vector_store:test_embedding",
            mapping={
                "content": test_text,
                "embedding": np_embedding
            }
        )
        print("Embedding saved successfully!")
        
        # 저장된 임베딩 확인 (content만 디코딩)
        print("\nVerifying stored embedding...")
        stored_data = redis_conn.hgetall("artist_vector_store:test_embedding")
        print(f"Stored content: {stored_data[b'content'].decode('utf-8')}")
        print(f"Embedding exists: {b'embedding' in stored_data}")
        
    except Exception as e:
        print(f"Error during embedding test: {e}")

if __name__ == "__main__":
    test_data_insertion()
    test_embedding_creation()
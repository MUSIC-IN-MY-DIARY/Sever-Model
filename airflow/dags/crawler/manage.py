from redis import Redis
import os

class DataManager:
    def __init__(self, index_name='artist_vector_store'):
        """
        Redis와 연결된 데이터 매니저 초기화
        """

        redis_host, redis_port, redis_password = os.getenv('REDIS_HOST', 'localhost'), \
            os.getenv('REDIS_PORT', '1234'), \
            os.getenv('REDIS_PASSWORD', '<PASSWORD>')
        self.redis_conn = Redis(host=redis_host, port=redis_port, password=redis_password)
        self.index_name = index_name

    def save_song(self, song_data):
        """
        곡 데이터를 Redis에 저장 (인덱스 이름 추가)
        :param song_data: 곡 정보 딕셔너리
        """
        song_id = song_data['song_id']
        # 각 필드를 인덱스에 맞게 hset으로 저장
        for key, value in song_data.items():
            self.redis_conn.hset(f"{self.index_name}:song:{song_id}", key, value)
        print(f"Saved song '{song_data['title']}' to Redis")

    def save_artist(self, artist_id, artist_data):
        """
        아티스트 데이터를 Redis에 저장 (인덱스 이름 추가)
        :param artist_id: 아티스트 ID
        :param artist_data: 아티스트 정보 딕셔너리
        """
        # 각 필드를 인덱스에 맞게 hset으로 저장
        for key, value in artist_data.items():
            self.redis_conn.hset(f"{self.index_name}:artist:{artist_id}", key, value)
        print(f"Saved artist '{artist_data['name']}' to Redis")

    def get_song(self, song_id):
        """
        곡 데이터를 Redis에서 조회
        :param song_id: 곡 ID
        :return: 곡 정보 딕셔너리
        """
        return self.redis_conn.hgetall(f"song:{song_id}")

    def get_artist(self, artist_id):
        """
        아티스트 데이터를 Redis에서 조회
        :param artist_id: 아티스트 ID
        :return: 아티스트 정보 딕셔너리
        """
        return self.redis_conn.hgetall(f"artist:{artist_id}")
from redis import Redis

class DataManager:
    def __init__(self, redis_host='localhost', redis_port=6379):
        """
        Redis와 연결된 데이터 매니저 초기화
        """
        self.redis_conn = Redis(host=redis_host, port=redis_port)

    def save_song(self, song_data):
        """
        곡 데이터를 Redis에 저장
        :param song_data: 곡 정보 딕셔너리
        """
        song_id = song_data['song_id']  # song_id 필드를 사용
        # 각 필드를 hset으로 저장
        for key, value in song_data.items():
            self.redis_conn.hset(f"song:{song_id}", key, value)
        print(f"Saved song '{song_data['title']}' to Redis")

    def save_artist(self, artist_id, artist_data):
        """
        아티스트 데이터를 Redis에 저장
        :param artist_id: 아티스트 ID
        :param artist_data: 아티스트 정보 딕셔너리
        """
        # 각 필드를 hset으로 저장
        for key, value in artist_data.items():
            self.redis_conn.hset(f"artist:{artist_id}", key, value)
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
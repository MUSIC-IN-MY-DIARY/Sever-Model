from redis import Redis
class DataManager:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_conn = Redis(host=redis_host, port=redis_port)

    def save_song(self, song_data):
        # songId를 키로 사용하여 Redis에 저장
        song_id = song_data['songId']
        self.redis_conn.hmset(f"song:{song_id}", song_data)

    def save_artist(self, artist_id, artist_data):
        # artistId를 키로 사용하여 Redis에 저장
        self.redis_conn.hmset(f"artist:{artist_id}", artist_data)

    def get_song(self, song_id):
        return self.redis_conn.hgetall(f"song:{song_id}")

    def get_artist(self, artist_id):
        return self.redis_conn.hgetall(f"artist:{artist_id}")
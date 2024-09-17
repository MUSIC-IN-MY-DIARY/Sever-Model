import redis
from redis.exceptions import RedisError
from typing import List, Dict

class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def create_index(self, index_name: str, schema: List[str]):
        try:
            self.client.execute_command(
                'FT.CREATE',
                index_name, 'ON', 'HASH', 'PREFIX', 1, 'artist:', 'SCHEMA', *schema
            )
        except RedisError as e:
            print(f'Error creating index: {e}')

    def insert_data(self, index_name: str, data: List[Dict]):
        for idx, item in enumerate(data, 1):
            artist_id = f'artist:{idx}'
            try:
                self.client.hset(artist_id, mapping=item)
            except RedisError as e:
                print(f'Error inserting data: {e}')

    def search_data(self, index_name: str, query: str):
        try:
            return self.client.execute_command('FT.SEARCH', index_name, query)
        except RedisError as e:
            print(f'Error searching data: {e}')
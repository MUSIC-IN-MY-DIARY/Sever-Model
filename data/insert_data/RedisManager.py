import redis
from redis.exceptions import RedisError
from typing import List, Dict
import os

class RedisManager:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0))
        )

    def create_index_if_not_exists(self, index_name: str, schema: List[str]):
        try:
            # Check if index exists, create if not
            indexes = self.client.execute_command('FT._LIST')
            if index_name not in indexes:
                self.client.execute_command('FT.CREATE', index_name, 'ON', 'HASH', 'PREFIX', 1, 'artist:', 'SCHEMA', *schema)
                print(f"Created index: {index_name}")
        except RedisError as e:
            print(f'Error creating index: {e}')

    def insert_data(self, index_name: str, artist_id: str, data: Dict):
        try:
            self.client.hset(artist_id, mapping=data)
            print(f"Data inserted for {artist_id}")
        except RedisError as e:
            print(f'Error inserting data for {artist_id}: {e}')

    def search_data(self, index_name: str, query: str):
        try:
            return self.client.execute_command('FT.SEARCH', index_name, query)
        except RedisError as e:
            print(f'Error searching data: {e}')
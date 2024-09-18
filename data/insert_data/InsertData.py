import json
from .RedisManager import RedisManager
from typing import List, Dict

class InsertData:
    def __init__(self, filename: str):
        self.filename = filename
        self.redis_manager = RedisManager()

    def load_data(self) -> List[Dict]:
        try:
            with open(self.filename, 'r', encoding='UTF-8') as f:
                return json.load(f)
        except IOError as e:
            print(f'Error: failed to load json file {self.filename}, {e}')
            return []

    def insert_data(self):
        data = self.load_data()
        if data:
            schema = [
                '이름', 'TEXT', 'WEIGHT', '1.0',
                '본명', 'TEXT', 'WEIGHT', '0.8',
                '생년월일', 'TEXT', 'WEIGHT', '0.5',
                '데뷔', 'TEXT', 'WEIGHT', '0.6',
                '그룹', 'TEXT', 'WEIGHT', '1.0',
                '히트곡', 'TEXT', 'WEIGHT', '0.9',
                '특징', 'TEXT', 'WEIGHT', '1.2'
            ]
            self.redis_manager.create_index_if_not_exists('ArtistIndex', schema)
            for item in data:
                artist_id = f"artist:{item['이름']}"
                processed_item = {k: ', '.join(v) if isinstance(v, list) else v for k, v in item.items()}
                self.redis_manager.insert_data('ArtistIndex', artist_id, processed_item)

    def main(self):
        self.insert_data()
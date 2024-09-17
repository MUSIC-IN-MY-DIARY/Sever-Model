import json
from data.RedisManager import RedisManager
from typing import Dict, List


class InsertData:
    def __init__(self, filename: str):
        self.filename = filename
        self.redis_manager = RedisManager()

    def load_data(self) -> Dict:
        try:
            with open(self.filename, 'r', encoding='UTF-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'Error: failed to load json file {self.filename}, {e}')
            return {}

    def insert_data(self, data: List[Dict]):
        schema = [
            '이름', 'TEXT', 'WEIGHT', '1.0',
            '본명', 'TEXT', 'WEIGHT', '0.8',
            '생년월일', 'TEXT', 'WEIGHT', '0.5',
            '데뷔', 'TEXT', 'WEIGHT', '0.6',
            '그룹', 'TEXT', 'WEIGHT', '1.0',
            '히트곡', 'TEXT', 'WEIGHT', '0.9',
            '특징', 'TEXT', 'WEIGHT', '1.2'
        ]
        try:
            self.redis_manager.create_index('ArtistIndex', schema)
        except Exception as e:
            print(f'Index creation failed: {e}')

        # 데이터 리스트 각 요소를 처리
        for item in data:
            # 리스트가 아닌 값을 콤마로 분리된 문자열로 변환
            processed_item = {key: ', '.join(value) if isinstance(value, list) else value for key, value in
                              item.items()}
            try:
                self.redis_manager.insert_data('ArtistIndex', processed_item)
            except Exception as e:
                print(f'Error inserting data: {e}')
    def main(self):
        data = self.load_data()
        if data:
            self.insert_data(data)


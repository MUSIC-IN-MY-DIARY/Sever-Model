import json
from .RedisManager import RedisVectorStore
from typing import List, Dict

class InsertData:
    def __init__(self, filename: str):
        """
        InsertData 클래스 초기화
        :param filename: JSON 파일 경로
        """
        self.filename = filename
        self.data = []
        self.vector_store = RedisVectorStore()  # RedisVectorStore 인스턴스 생성

    def load_data(self) -> List[Dict]:
        """
        JSON 파일을 읽어 데이터를 로드
        :return: 로드된 데이터 리스트
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)  # 파일을 JSON 형태로 로드
                print(f'Data loaded successfully from {self.filename}')
        except IOError as e:
            print(f'Error reading the file: {e}')
            self.data = []
        return self.data

    def insert_data(self, index_name: str = 'artist_vector_store'):
        """
        Redis에 데이터 삽입
        :param index_name: Redis 인덱스 이름
        :return: None
        """
        if not self.data:
            print('No data found. Please load data first using load_data()')
            return

        # 인덱스 생성
        try:
            self.vector_store.create_vector_index()
        except Exception as e:
            print(f"Error creating index: {e}")
            return

        # 각 아티스트 데이터를 삽입
        for idx, artist in enumerate(self.data):
            artist_id = f"{index_name}:artist_{idx+1}"
            try:
                self.vector_store.insert_data(artist_id, artist)
                print(f"Inserted artist {artist['이름']} into Redis")
            except Exception as e:
                print(f"Failed to insert artist {artist['이름']}: {e}")

    def run(self):
        """전체 실행 흐름 제어"""
        self.load_data()
        self.insert_data()
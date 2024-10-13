from config.Authentication import AuthenticationData
from cralwer.crawler import Crawler
from cralwer.manage import DataManager
from cralwer.parser import Parser
from redis_data.RedisManager import RedisVectorStore

import requests
import time

class Controller:
    def __init__(self):
        auth_data = AuthenticationData()
        self.base_url = auth_data.get_base_url()
        self.chart_url = f"{self.base_url}{auth_data.get_chart_url()}"
        self.detail_url = f"{self.base_url}{auth_data.get_detail_url()}"
        self.artist_url = f"{self.base_url}{auth_data.get_artist_url()}"
        self.headers = auth_data.get_headers()

        self.crawler = Crawler(self.base_url, self.headers)
        self.parser = Parser()
        self.manage = DataManager()

        self.redis_manager = RedisVectorStore()

    def main(self):
        # 인덱스 생성

        try:
            self.redis_manager.create_vector_index()
        except Exception as e:
            print(f"Error creating index: {e}")

        # 차트 페이지 크롤링
        main_page = self.crawler.fetch_page(self.chart_url)
        songs = self.parser.parse_main_page(main_page)


        for song in songs:
            # 곡 상세 정보 크롤링
            song_page = self.crawler.fetch_page(self.detail_url, params={'songId': song['song_id']})
            song_detail = self.parser.parse_song_detail(song_page)
            song['song_detail'] = song_detail

            # 아티스트 상세 정보 크롤링
            artist_page = self.crawler.fetch_page(self.artist_url, params={'artistId': song['artist_id']})
            artist_detail = self.parser.parse_artist_detail(artist_page)
            song['artist_detail'] = artist_detail

            # 데이터 저장 및 임베딩 처리
            try:
                self.redis_manager.insert_data(song['song_id'], song, data_type='song')  # 곡 데이터 저장
                self.redis_manager.insert_data(song['artist_id'], artist_detail, data_type='artist')  # 아티스트 데이터 저장
                print(f"'{song['title']}' 정보 저장 완료")
            except Exception as e:
                print(f"Error inserting data for '{song['title']}': {e}")

            # 3초 간격으로 크롤링
            time.sleep(3)

if __name__ == '__main__':
    controller = Controller()
    controller.main()
from config.Authentication import AuthenticationData
from .crawler import Crawler
from .parser import Parser
from .manage import DataManager

# Module

import time

class Controller:
    def __init__(self):
        auth_data = AuthenticationData()
        self.base_url = auth_data.get_base_url()
        self.chart_url = f"{self.base_url}{auth_data.get_chart_url()}"
        self.detail_url = f"{self.base_url}{auth_data.get_detail_url()}"
        self.artist_url = f"{self.base_url}{auth_data.get_artist_url()}"
        self.headers = auth_data.get_headers()

        self.crawler = Crawler(self.headers)
        self.parser = Parser()
        self.manage = DataManager()

    def main(self):
        main_page = self.crawler.fetch_page(self.chart_url)
        songs = self.parser.parse_main_page(main_page)

        for song in songs:
            # 곡 상세 정보 크롤링
            song_page = self.crawler.fetch_page(self.detail_url, params={'songId': song['songId']})
            song_detail = self.parser.parse_song_detail(song_page)
            song['song_detail'] = song_detail

            # 아티스트 상세 정보 크롤링
            artist_page = self.crawler.fetch_page(self.artist_url, params={'artistId': song['artistId']})
            artist_detail = self.parser.parse_artist_detail(artist_page)
            song['artist_detail'] = artist_detail

            # 데이터 저장
            self.manage.save_song(song)
            self.manage.save_artist(song['artistId'], artist_detail)

            print(f"'{song['title']}' 정보 저장 완료")
            time.sleep(3)

if __name__ == '__main__':
    Controller = Controller()
    Controller.main()

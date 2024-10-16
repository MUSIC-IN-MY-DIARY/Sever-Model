# config/authentication_data.py

import os
from dotenv import load_dotenv


class AuthenticationData:
    def __init__(self):

        self.base_url = os.getenv('BASE_URLS')
        self.chart_url = os.getenv('CHART_URL')
        self.detail_url = os.getenv('DETAIL_URL')
        self.artist_url = os.getenv('ARTIST_URL')
        self.user_agent = os.getenv('AGENT')
        self.token = os.getenv('OPENAI_API_KEY')

        self.redis_host = os.getenv('REDIS_HOST')
        self.redis_port = os.getenv('REDIS_PORT')

        # # 환경 변수 체크
        # if not all([self.base_url, self.chart_url, self.detail_url, self.artist_url, self.user_agent]):
        #     raise ValueError("환경 변수 설정이 제대로 되지 않았습니다.")

    def get_conn(self):
        return self.redis_host,self.redis_port

    def get_token(self):
        return self.token

    def get_base_url(self):
        return self.base_url

    def get_chart_url(self):
        return self.chart_url

    def get_detail_url(self):
        return self.detail_url

    def get_artist_url(self):
        return self.artist_url

    def get_headers(self):
        return {
            'User-Agent': self.user_agent
        }
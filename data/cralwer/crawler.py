import requests

class Crawler:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.session = reqeusts.Session()

    def fetch_page(self, url, params=None):
        reseponse = self.session.get(url, headers=self.headers)
        reseponse.raise_for_status() # 에러 발생시 처리
        return reseponse.text

# API key 통합 보관함
from dotenv import load_dotenv
import os
from typing import List, Dict

class Authentication:
    def __init__(self):
        load_dotenv("/Users/uicheol_hwang/Sever-Model/api/common/.env")
    def get_token(self: str) -> str:
        return os.getenv('OPENAI_API_KEY')

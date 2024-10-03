# API key 통합 보관함
from dotenv import load_dotenv
import os
from typing import List, Dict

class Authentication:
    def __init__(self):
        load_dotenv("/Users/uicheol_hwang/Sever-Model/config/Auth/.env")

    @classmethod
    def get_token(cls : str) -> str:
        return os.getenv('OPENAI_API_KEY')

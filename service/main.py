import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# root_path 설정 추가
app = FastAPI(root_path="/api/v2")  # root_path 설정

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터에 prefix 추가
from api.router.question.question import question_router
from api.router.generate.generate import generate_router

# prefix="/api" 제거 (root_path가 이미 /api를 처리)
app.include_router(question_router)
app.include_router(generate_router)

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# default Settings for Fastapi

from api.router.question.question import question_router
from api.router.question.test import test_router
# Modules

app = FastAPI(root_path='/api/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(question_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
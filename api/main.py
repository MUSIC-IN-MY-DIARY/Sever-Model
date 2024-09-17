import uvicorn


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# default Settings for Fastapi

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def testing_get():
    return {"say" : "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
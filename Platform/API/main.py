from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

# ===== LLM 모델 import =====

# =====

# 정보 형식 정의
## user_message: str
class MessageResponse(BaseModel):
    message: str


@app.get("/")
async def get_root() -> str:
    return {"message": "root"}

@app.post("/conversation")
async def post_message(request: MessageResponse) -> MessageResponse:
    print(request)
    input_message = request.message

    answer = f"{input_message}를 받았고, 반환되었습니다."

    return { "message": answer }
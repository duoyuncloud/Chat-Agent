# main_claude.py
# 本文件为 Claude4（Claude 3 Opus）云端大模型后端，适用于高质量云端推理、复杂任务等场景。
# 需要用户输入 Claude API Key（sk-ant-...）。

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import logging

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    api_key: str
    model: str = "claude-3-opus-20240229"  # default to Claude 3 Opus

class ChatResponse(BaseModel):
    response: str

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main_claude")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.api_key or not request.api_key.startswith("sk-ant-"):
        return ChatResponse(response="Claude API key not set or invalid. Please input a valid API key (sk-ant-...)")
    headers = {
        "x-api-key": request.api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": request.model,
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": request.message}
        ]
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(ANTHROPIC_API_URL, headers=headers, json=data, timeout=60.0)
            if response.status_code != 200:
                # Claude API 错误友好提示
                try:
                    err_json = response.json()
                    err_msg = err_json.get("error", {}).get("message") or err_json.get("error", str(response.text))
                except Exception:
                    err_msg = response.text
                logger.warning(f"Claude API error: {err_msg}")
                return ChatResponse(response=f"Claude API error: {err_msg}")
            result = response.json()
            try:
                reply = result["content"][0]["text"]
            except Exception:
                reply = str(result)
            return ChatResponse(response=reply)
    except Exception as e:
        logger.error(f"Exception in Claude chat: {e}")
        return ChatResponse(response=f"❌ Internal error: {e}") 
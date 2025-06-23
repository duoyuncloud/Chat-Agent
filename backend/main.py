from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print("Received request:", request.message)
    async with httpx.AsyncClient() as client:
        print("Sending request to Ollama...")
        async with client.stream(
            "POST",
            "http://localhost:11434/api/chat",
            json={
                "model": "llama2:latest",
                "messages": [
                    {"role": "user", "content": request.message}
                ]
            },
            timeout=120.0
        ) as response:
            print("Got response from Ollama, reading lines...")
            reply = ""
            async for line in response.aiter_lines():
                print("Line:", line)
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            reply += data["message"]["content"]
                    except Exception as e:
                        print("Error parsing line:", e)
            if not reply:
                reply = "No response from model."
            print("Final reply:", reply)
            return ChatResponse(response=reply)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import uvicorn
from dotenv import load_dotenv

from sera.llm.client import LLMClient

load_dotenv()

app = FastAPI(title="Sera Neural Interface API")

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM Client
client = LLMClient()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
async def root():
    return {"status": "online", "service": "Sera Neural Interface"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Convert Pydantic models to dicts for the LLMClient
        messages_dict = [m.model_dump() for m in request.messages]
        
        # Generate response from Sera
        response_text = await client.generate_response(messages_dict)
        
        return {"role": "assistant", "content": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def serve_server(host="0.0.0.0", port=8000):
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)
    await server.serve()

def start_server(host="0.0.0.0", port=8000):
    """Sync entry point for development/scripts."""
    import asyncio
    asyncio.run(serve_server(host=host, port=port))

if __name__ == "__main__":
    start_server()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio, json, os, sys
from typing import AsyncGenerator
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ModelClientStreamingChunkEvent

# import model client from AgenChat
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from AgenChat.llms import get_model_client

root_dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(root_dir, ".env"))

app = FastAPI(title="Yommy Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def sse_line(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

async def generate_stream(message: str) -> AsyncGenerator[str, None]:
    try:
        client = get_model_client()
        agent = AssistantAgent(
            name="yommy_agent",
            model_client=client,
            system_message="你是 Yommy Chat，一个简洁且有帮助的助手，按用户语言作答。",
            model_client_stream=True,
        )
        meta = {
            "meta": {
                "model": os.getenv("MODEL") or "deepseek-chat",
                "base_url": os.getenv("API_BASE_URL") or os.getenv("BASE_URL") or "https://api.deepseek.com/v1",
                "source": "AgentChat",
            }
        }
        yield sse_line(meta)
        async for event in agent.run_stream(task=message):
            if isinstance(event, ModelClientStreamingChunkEvent):
                yield sse_line({"content": event.content})
        yield "data: [DONE]\n\n"
    except Exception as e:
        meta = {
            "meta": {
                "model": "simulate",
                "base_url": "",
                "source": "fallback",
                "error": str(e),
            }
        }
        yield sse_line(meta)
        chunks = [
            "你好！这是演示模式输出。 ",
            "当前未配置真实模型密钥或服务暂不可用。 ",
            "你仍可浏览界面与流式效果。 ",
            "配置完成后将自动切换到真实模型。 ",
        ]
        for c in chunks:
            await asyncio.sleep(0.2)
            yield sse_line({"content": c})
        yield "data: [DONE]\n\n"

@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        generate_stream(req.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": os.getenv("MODEL", "unknown")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")), reload=True)

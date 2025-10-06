from fastapi import FastAPI
from routers import health, chat, completions, embeddings, rerank

# ✅ FastAPI 앱 초기화
app = FastAPI(title="Mock OpenAI-Compatible LLM Server")

# ✅ Router 등록
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(completions.router)
app.include_router(embeddings.router)
app.include_router(rerank.router)


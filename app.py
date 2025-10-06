from fastapi import FastAPI
from routers import health, chat, completions, embeddings, rerank

app = FastAPI(title="Mock OpenAI-Compatible LLM Server")

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(completions.router)
app.include_router(embeddings.router)
app.include_router(rerank.router)


from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/v1", tags=["Rerank"])

class RerankRequest(BaseModel):
    model: str
    query: str
    documents: List[str]

@router.post("/rerank")
async def rerank(req: RerankRequest):
    ranked = sorted(req.documents, key=lambda d: abs(len(d) - len(req.query)))
    return {
        "object": "list",
        "model": req.model,
        "data": [
            {"index": i, "document": doc, "score": 1.0 / (i + 1)}
            for i, doc in enumerate(ranked)
        ]
    }

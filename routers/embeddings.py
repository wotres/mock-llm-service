from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union, List
import hashlib

router = APIRouter(prefix="/v1", tags=["Embeddings"])

class EmbeddingRequest(BaseModel):
    model: str
    input: Union[str, List[str]]  # ✅ 문자열 or 문자열 배열 모두 허용


def mock_embedding_vector(text: str):
    """간단한 해시 기반 벡터 (mock)"""
    digest = hashlib.sha256(text.encode()).digest()
    # 8차원 예시 벡터
    return [round(b / 255, 4) for b in digest[:8]]


@router.post("/embeddings")
async def create_embeddings(req: EmbeddingRequest):
    """
    OpenAI Embeddings API 스타일 모방:
    - input: string or list[string]
    - 반환 구조: data: [{object, embedding, index}, ...]
    """
    inputs = req.input if isinstance(req.input, list) else [req.input]

    data = []
    for i, text in enumerate(inputs):
        vector = mock_embedding_vector(text)
        data.append({
            "object": "embedding",
            "index": i,
            "embedding": vector
        })

    return {
        "object": "list",
        "model": req.model,
        "data": data,
        "usage": {
            "prompt_tokens": len(inputs),
            "total_tokens": len(inputs)
        }
    }

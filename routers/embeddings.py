from typing import Union, List
from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

router = APIRouter(prefix="/v1", tags=["Embeddings"])

# ✅ 실제 모델 로드 (서버 시작 시 한 번만)
model = SentenceTransformer("all-MiniLM-L6-v2")


class EmbeddingRequest(BaseModel):
    model: str
    input: Union[str, List[str]]  # 문자열 or 문자열 배열 모두 허용


def real_embedding_vector(text: str):
    """SentenceTransformer 기반 실제 384차원 벡터 생성"""
    vector = model.encode(text)
    return vector.tolist()  # numpy array → list 변환


@router.post("/embeddings")
async def create_embeddings(req: EmbeddingRequest):
    """
    OpenAI Embeddings API 스타일:
    - input: string or list[string]
    - 반환 구조: data: [{object, embedding, index}, ...]
    """
    inputs = req.input if isinstance(req.input, list) else [req.input]

    data = []
    for i, text in enumerate(inputs):
        vector = real_embedding_vector(text)
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

import asyncio
import json
from typing import Optional, AsyncGenerator

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/v1", tags=["Completions"])


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = 50
    stream: Optional[bool] = False


# mock 스트리밍 유틸
async def mock_stream_completion(prompt: str) -> AsyncGenerator[dict, None]:
    reply = f"Mock completion for: {prompt}"
    for ch in reply:
        chunk = {
            "id": "cmpl-mock",
            "object": "text_completion.chunk",
            "model": "mock-model",
            "choices": [
                {
                    "text": ch,
                    "index": 0,
                    "finish_reason": None
                }
            ]
        }
        await asyncio.sleep(0.03)
        yield chunk
    final = {
        "id": "cmpl-mock",
        "object": "text_completion.chunk",
        "model": "mock-model",
        "choices": [
            {
                "text": "",
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }
    yield final


@router.post("/completions")
async def completions(req: CompletionRequest):
    if not req.stream:
        text = req.prompt.strip()
        mock_output = f"Mock completion for: {text}"
        return {
            "id": "cmpl-mock",
            "object": "text_completion",
            "model": req.model,
            "choices": [
                {"text": mock_output, "index": 0, "finish_reason": "stop"}
            ]
        }

    # 스트리밍 모드
    async def event_gen():
        async for chunk in mock_stream_completion(req.prompt):
            yield f"data: {json.dumps(chunk)}\n\n"
    from fastapi import responses
    return responses.StreamingResponse(event_gen(), media_type="text/event-stream")

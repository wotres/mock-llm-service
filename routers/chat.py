from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator, Optional
import asyncio
import json

router = APIRouter(prefix="/v1/chat", tags=["Chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False  # 기본 비스트리밍 모드

# 내부 유틸: mock 응답 스트리밍 제너레이터
async def mock_stream_response(user_message: str) -> AsyncGenerator[dict, None]:
    """
    예: 한 글자씩 천천히 보내는 mock 응답
    실제론 LLM 토큰 하나씩 보내는 구조로 바꾸면 됨.
    """
    reply = f"Echo (stream): {user_message}"
    # 예: 각 문자 또는 단어를 나눠서 청크로 보냄
    for ch in reply:
        chunk = {
            "id": "chatcmpl-mock",
            "object": "chat.completion.chunk",
            "model": "mock-model",
            "choices": [
                {
                    "delta": {"content": ch},
                    "index": 0,
                    "finish_reason": None
                }
            ]
        }
        await asyncio.sleep(0.05)  # 지연 시뮬레이션
        yield chunk
    # 마지막 종료 청크
    final = {
        "id": "chatcmpl-mock",
        "object": "chat.completion.chunk",
        "model": "mock-model",
        "choices": [
            {
                "delta": {},  # delta.content 없음
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }
    yield final

@router.post("/completions")
async def chat_completion(req: ChatRequest, request: Request):
    """
    stream=False: 전체 응답 반환
    stream=True: SSE 스트리밍 응답
    """
    # 추출 예: 유저 메시지 선택
    user_message = ""
    for m in req.messages:
        if m.role == "user":
            user_message = m.content
            break

    # 비스트리밍 모드
    if not req.stream:
        reply = f"Echo (full): {user_message}"
        return {
            "id": "chatcmpl-mock",
            "object": "chat.completion",
            "model": req.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": reply},
                    "finish_reason": "stop",
                }
            ]
        }

    # 스트리밍 모드: SSE 형식 응답
    async def event_generator():
        async for chunk in mock_stream_response(user_message):
            # SSE 형식: "data: {json}\n\n"
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")


## 로컬 실행
```bash
$ pip install -r requirements.txt
$ uvicorn app:app --host 0.0.0.0 --port 8888 --reload
# http://localhost:8888/docs 확인
```

## Docker 실행
```bash
# 이미지 빌드
$ docker build -t mock-llm-service:ai-assistant .
# 컨테이너 실행
$ docker run -d -p 8888:8888 --name mock-llm-service mock-llm-service:ai-assistant
# 컨테이너 정지
$ docker stop mock-llm-service
# 컨테이너 시작
$ docker start mock-llm-service
# 컨테이너 삭제
$ docker rm -f mock-llm-service

# 컨테이너 접속
$ docker run -it --rm mock-llm-service:ai-assistant /bin/bash
## 컨테이너 내부 copy 된 폴더 확인 및 용량 확인
$ du -h --max-depth=1
$ ls -lh
```

## Kubernetes 실행 및 배포 운영
* ai-assistant-k8s private repo 참조

## 테스트
```bash
# chat
## Non-streaming
$ curl -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

## Streaming
$ curl -N -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock",
    "messages": [{"role": "user", "content": "Streaming test!"}],
    "stream": true
  }' 

# completions
## Non-streaming
$ curl -X POST http://localhost:8888/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock",
    "prompt": "Once upon a time"
  }'
## Streaming
$ curl -N -X POST http://localhost:8888/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock",
    "prompt": "Stream me please!",
    "stream": true
  }'

# Embeddings
## Single
$ curl -X POST http://localhost:8888/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-embedding",
    "input": "This is a test"
  }'
  
## Batch
$ curl -X POST http://localhost:8888/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-embedding",
    "input": [
      "This is a test",
      "Another test"
    ]
  }'

# Rerank
$ curl -X POST http://localhost:8888/v1/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mock-reranker",
    "query": "apple",
    "documents": [
      "apple pie",
      "banana split",
      "apple juice",
      "grape soda"
    ]
  }'
  
```
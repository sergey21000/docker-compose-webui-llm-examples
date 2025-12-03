
Готовые популярные комбинации сервисов в одном compose файле

## 🚀 Быстрый старт

***1) Клонирование репозитория и копирование env**
```sh
git clone https://github.com/sergey21000/docker-compose-webui-llm-examlples
cd docker-compose-webui-llm-examlples
cp env.example .env
cp data/anythingllm/env.example data/anythingllm/env
```

**2) Запуск сервисов**  
- С поддержккой CPU
  ```sh
  docker compose up -d
  ```
- С поддержккой CUDA
  ```sh
  docker compose -f compose.cuda.yml up -d
  ```


---
Вариант запуска сервисов без указания `-f compose.cuda.yml`

Установка переменной `COMPOSE_FILE`
- Linux
  ```sh
  export COMPOSE_FILE=compose.cuda.yml
  ```
- Windows PowerShell
  ```ps1
  $env:COMPOSE_FILE="compose.cuda.yml"
  ```

Запуск
```sh
docker compose up -d
```


---
По умолчанию сервисы доступны по адресам:
- AnythingLLM WebUI: http://127.0.0.1:3001
- Open WebUI: http://127.0.0.1:3000
- llama.cpp WebUI: http://127.0.0.1:8080
- llama.cpp API: http://127.0.0.1:8080/v1
- Ollama BASE URL: http://127.0.0.1:11434
- vLLM API: http://127.0.0.1:8000/v1
- vLLM Models http://127.0.0.1:8000/v1/models
- Qdrant Dashboard: http://127.0.0.1:6333/dashboard
- Infinity Embeddings Swagger: http://127.0.0.1:7997/docs
- Infinity API: http://localhost:7997/v1
- MCP Server API: http://127.0.0.1:9000/v1









# Ollama

Запуск LLM через библиотеку Ollama:
- [**Ollama**](https://github.com/ollama/ollama) - запуск LLM моделей


## 🐳🚀 Быстрый старт

Клонирование репозитория
```
git clone https://github.com/sergey21000/webui-llm-examlples
cd webui-llm-examlples/anythingllm_ollama
```

Скопировать файл `.env` с переменными окружения
```sh
cd openwebui_ollama
cp env.example .env
```
Редактировать переменные окружения в файле `.env` при необходимости (ссылки на документацию внутри файла `.env`)

Запуск сервисов
- Запуск с поддержкой CPU
  ```sh
  docker compose up -d
  ```
- Запуск с поддержкой CUDA
  ```sh
  docker compose -f compose.cuda.yml up -d
  ```

Загрузка моделей для Ollama  
https://ollama.com/library
```
docker exec -it ollama ollama pull gemma3:4b
```
Список загруженных моделей Ollama
```
docker exec -it ollama ollama list
```

Проверить статус сервисов
```sh
docker compose ps
```
Просмотр логов запуска сервисов
```
docker compose logs -f
```

По умолчанию сервис будут доступны по адресу:
- Ollama API: http://127.0.0.1:11434


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

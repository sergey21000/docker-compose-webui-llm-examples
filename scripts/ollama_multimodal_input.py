# https://docs.ollama.com/capabilities/vision#python

from pathlib import Path
from loguru import logger

from ollama import chat
from ollama import ChatResponse


# системный промт (опционально)
system_prompt = ''
# основной промт
prompt = 'Что изображено на картинке?'

# путь до картинки
image_path = './mcp_server/data/images/donkey.jpg'

# или base64 картинки
# img = base64.b64encode(Path(image_path).read_bytes()).decode()

# или байты картинки
# img = Path(image_path).read_bytes()

# сообщения для подачи в модель / история переписки
messages = []
if system_prompt:
    messages.append({'role': 'system', 'content': system_prompt})
messages.append({'role': 'user', 'content': prompt, 'images': [image_path]})

# модель из Ollama list
model = 'gemma3:4b'

# генерация ответа модели в режиме стриминга
stream_chat: ChatResponse = chat(
    model=model,
    messages=messages,
    think=False,
    stream=True,
)

# получение ответа по одному токену
response_message = ''
for part in stream_chat:
    token = part['message']['content']
    response_message += token
    print(token, end='', flush=True)

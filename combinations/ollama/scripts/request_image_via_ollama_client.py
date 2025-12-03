# pip install ollama
from ollama import chat
from pathlib import Path

image_path = 'ollama_data/donkey.jpg'

stream_chat = chat(
  model='gemma3:4b',
  stream=True,
  messages=[
    {
      'role': 'user',
      'content': 'Что изображено на картинке?',
      'images': [image_path],
    }
  ],
)

response_text = ''
for part in stream_chat:
    token = part['message']['content']
    response_text += token
    
    print(token, end='', flush=True)

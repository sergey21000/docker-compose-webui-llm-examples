import requests
import json


url = "http://127.0.0.1:11434/api/chat"
data = {
    "model": "gemma3:4b",
    "messages": [
        {"role": "user", "content": "Что ты умеешь?"}
    ]
}
response = requests.post(url, json=data)
response.raise_for_status()
print(f'Response JSON text :{response.text}')

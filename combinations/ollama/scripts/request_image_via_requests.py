import time
import json
import base64
from pathlib import Path

import requests


url = "http://localhost:11434/api/chat"
image_path = '../data/images/donkey.jpg'
image_base64 = base64.b64encode(Path(image_path).read_bytes()).decode()
data = {
    "model": "gemma3:4b",
    "messages": [
        {
            "role": "user",
            "content": "Что изображено на картинке?",
            "images": [image_base64],
            "options": {"seed": 111, "temperature": 0},
        }
    ]
}
response = requests.post(url, json=data)
response.raise_for_status()
response_text = ""
for line in response.iter_lines():
    if line:
        json_response = json.loads(line)
        if json_response.get("done"):
            break
        token = json_response.get("message", {}).get("content", "")
        response_text += token
        time.sleep(0.1)
        
        print(token, end='', flush=True)

# print(response_text)
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
response_text = ""
for line in response.iter_lines():
    if line:
        json_response = json.loads(line)
        if json_response.get("done"):
            break
        token = json_response.get("message", {}).get("content", "")
        response_text += token
        
        print(token)

# print(response_text)

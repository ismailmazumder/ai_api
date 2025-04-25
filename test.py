import requests

url = "http://127.0.0.1:5000/ask"

payload = {
    "question": "What is the capital of France?"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Error parsing JSON response:", e)
    print("Raw Text Response:", response.text)

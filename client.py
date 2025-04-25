import requests

# Define the Flask server URL
FLASK_URL = "https://ai-api-al6k.onrender.com/ask"

# Define the payload to send to the Flask server
payload = {
    "text": "how many people bangladeshi student  killed in july 2024. ",
}

# Send a POST request to the Flask server
try:
    response = requests.post(FLASK_URL, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    #print("Response from server:", response.json()['responses'])
except requests.exceptions.RequestException as e:
    print("Error:", e)
number = ""
link_parts = []
is_comma = False

response_data = response.json()['responses']

number_parts = []
link_parts = []
is_number_done = False

for item in response_data:
    if 'text' in item:
        text = item['text'].strip()

        if not is_number_done and all(c in "0123456789," for c in text.replace(" ", "")):
            number_parts.append(text)
        else:
            is_number_done = True
            link_parts.append(text)

# Join number parts and remove commas
number_str = ''.join(number_parts).replace(',', '')
number = int(number_str)

# Join link parts
full_link = ''.join(link_parts).replace(' ', '')

print("Number:", number)
print("Link:", full_link)

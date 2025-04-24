from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="xai-qFzyVGpo6VhCtwTsJxX7LxygFrGFAD1oImsSumWHK3JcEtXUjVHjbztJUJFwWT9gNDOrw4AeXa1MgkQF",
    base_url="https://api.x.ai/v1",
)

@app.route('/')
def home():
    return jsonify({"message": "API is running!"})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    completion = client.chat.completions.create(
        model="grok-3-latest",
        messages=[
            {"role": "system", "content": "You are a PhD-level mathematician."},
            {"role": "user", "content": question},
        ],
    )

    answer = completion.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from websocket import create_connection
import json
import logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

WS_URL = "wss://copilot.microsoft.com/c/api/chat?api-version=2"
WS_HEADERS = {
    "Accept-Charset": "UTF-8",
    "Accept": "*/*",
    "Upgrade": "websocket",
    "Connection": "Upgrade",
    "User-Agent": "CopilotNative/30.0.430409001 (Android 15; Google; Pixel 7 Pro)",
    "X-Search-UILang": "en-US",
    "sentry-trace": "trace-id",
    "baggage": "some-baggage",
    "Host": "copilot.microsoft.com",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "_EDGE_V=1; MUID=your-muid"
}

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True, silent=True) or {}
    logging.info("Received request: %s", data)

    text = data.get("text") + " .(1st just the number In integer tha by a comma  source link(link should be in text,like abc.com/gaza,   nothing else)(tell the average number so i get the accurate number)"
    if not text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    conversation_id = data.get("conversationId", "dDr9f3Z673dwuywprvmUD")
    payload = {
        "event": "send",
        "content": [{"type": "text", "text": text}],
        "conversationId": conversation_id
    }

    try:
        ws = create_connection(WS_URL, header=WS_HEADERS)
        ws.settimeout(3)  # Set a timeout of 4 seconds for WebSocket operations
        ws.send(json.dumps(payload))
        print(text)
        logging.info("Message sent. Listening for all responses...")

        messages = []

        # Set a read limit to avoid infinite loop (can be adjusted or removed)
        for _ in range(20):  # Try receiving 4 messages max
            try:
                raw = ws.recv()
                if raw:
                    msg = json.loads(raw)
                    messages.append(msg)
                    print(msg)
            except Exception as e:
                logging.warning("WebSocket recv error or timeout: %s", e)
                break

        ws.close()
        return jsonify({"responses": messages})

    except Exception as e:
        logging.error("WebSocket error: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

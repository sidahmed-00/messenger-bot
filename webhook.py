from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "sido009"  # نفس التوكين في إعدادات فيسبوك

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Error: Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        print("🔔 Received message:", data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

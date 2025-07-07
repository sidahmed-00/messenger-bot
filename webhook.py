import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "sido009"
PAGE_ACCESS_TOKEN = "EAAKYtAyYyoABPAlevKlXyk8Jsk4ZB3gqH8L8f0Yv4jx9r5uuPhyFYkc1NliUJ1DnAQ2acUw7l7INR6oLcApr1Q0WHJ8G71we4fkesENbsOqJbzuRK2NB5SdWmAztLV9Ad2DXO2PFDxHOtNYO3Sj9X3oDK0HCAVJlpRU1ZA7AI3zh6aZCZCfBV1INWaY32qJeodjbJYlqiAZDZD"  # حط توكن صفحتك هنا

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

        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for message_event in entry["messaging"]:
                        sender_id = message_event["sender"]["id"]
                        if "message" in message_event:
                            send_message(sender_id, "مرحباً! أنا بوت تجريبي 😄")

        return "EVENT_RECEIVED", 200

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📨 Sent message response:", response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


import os
import requests
import openai
from flask import Flask, request
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()

# إعداد Flask
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# الرد على التحقق من Facebook
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
        print("🔔 Received:", data)

        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for message_event in entry["messaging"]:
                        sender_id = message_event["sender"]["id"]
                        if "message" in message_event and "text" in message_event["message"]:
                            user_message = message_event["message"]["text"]
                            response = get_openai_response(user_message)
                            send_message(sender_id, response)

        return "EVENT_RECEIVED", 200


# إرسال رسالة عبر Facebook
def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📨 Sent message:", response.json())


# الرد من OpenAI
def get_openai_response(message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # أو "gpt-4" لو عندك
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي يتكلم بالعربية."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        print("❌ OpenAI Error:", str(e))
        return "حدث خطأ أثناء الاتصال بـ ChatGPT."


# تشغيل السيرفر
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    def get_openai_response(message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي يتكلم بالعربية."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        print("❌ OpenAI Error:", str(e))  # هذا موجود
        import traceback
        traceback.print_exc()  # نضيف هذا باش نشوف التفاصيل
        return "حدث خطأ أثناء الاتصال بـ ChatGPT."





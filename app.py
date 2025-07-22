from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    user_msg = request.values.get("Body", "")
    user_number = request.values.get("From", "")

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_whatsapp = "whatsapp:+14155238886"

    gpt_response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer " + openai_api_key,
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Eres un agente de ventas amable y profesional."},
                {"role": "user", "content": user_msg}
            ]
        }
    )

    reply = gpt_response.json()["choices"][0]["message"]["content"]

    requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json",
        auth=(twilio_sid, twilio_token),
        data={
            "From": from_whatsapp,
            "To": user_number,
            "Body": reply
        }
    )

    return "OK", 200
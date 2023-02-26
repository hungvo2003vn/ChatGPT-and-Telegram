from flask import Flask, request
import requests
import openai
import Tokens as tks

app = Flask(__name__)

openai.api_key = tks.OpenAi
bot_token = tks.bot_token
my_url = tks.my_url
secret = tks.secret

@app.route("/")
def index():
    return "This is the index page. Send a POST request to /receive_message to chat with the bot."

@app.route("/{}".format(secret), methods=["GET", "POST"])
def receive_message():
    if request.method == "POST":
        update = request.get_json()
        chat_id = update["message"]["chat"]["id"]
        message = update["message"]["text"]
        respond_to_message(chat_id, message)
        return "OK"
    else:
        return "This is the receive_message page. Send a POST request to chat with the bot."

def respond_to_message(chat_id, message):
    response = generate_response(message)
    send_message(response, chat_id)

def send_message(message, chat_id):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message,
        }
    )

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    ).choices[0].text
    return response

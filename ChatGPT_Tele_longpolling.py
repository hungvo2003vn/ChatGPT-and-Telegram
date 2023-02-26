from flask import Flask
import requests
import openai
import time
import threading
import Tokens as tks

app = Flask(__name__)

openai.api_key = tks.OpenAi
bot_token = tks.bot_token
my_url = tks.my_url
update_offset = 0

#chat_id = "5040107670"
#group_chat_id = "-1001733189080"

def receive_message():
    global update_offset
    
    while True:
        result = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            params={"offset": update_offset}
        ).json()
    
        if len(result["result"]) > 0:
            for update in result["result"]:
                update_offset = update["update_id"] + 1
                chat_id = update["message"]["chat"]["id"]
                message = update["message"]["text"]
                thread = threading.Thread(target=respond_to_message, args=(chat_id, message))
                thread.start()
        
        time.sleep(3)

@app.route("/")
def start_receive_message():
    receive_message()
    return "OK"

def respond_to_message(chat_id, message):
    response = generate_response(message)
    send_message(response, chat_id)

def send_message(message, chat_id):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message,
            "url": "{my_url}/receive_message"
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


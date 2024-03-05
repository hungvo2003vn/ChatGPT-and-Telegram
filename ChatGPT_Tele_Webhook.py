from flask import Flask, request
import requests
import openai
from dotenv import load_dotenv
import os
# import Tokens as tk
# import re
# import time
import json
from pymongo import MongoClient

app = Flask('__name__')

load_dotenv()
openai.api_key = os.getenv('OpenAi')
bot_token = os.getenv('bot_token')
# secret = os.getenv('secret')
deployment_url = os.getenv('deployment_url')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

#Get database
client = MongoClient(CONNECTION_STRING)
dbname = client['messageDB']
initialize = {}

###########################---SET WEBHOOK---##################################
def setWebhook():
  msg = requests.post(
    f"https://api.telegram.org/bot{bot_token}/setWebhook",
    params={
      "url": deployment_url,
      "allow_updates": '["message", "edited_message", "channel_post", "edited_channel_post", "callback_query"]'
    }
  )
  msg.content["url"] = deployment_url
  msg.content["allow_updates"] = '["message", "edited_message", "channel_post", "edited_channel_post", "callback_query"]'
  return json.loads(msg.content)

print(setWebhook())
###########################################################################
def check_initDB(chat_id):
  global initialize
  chat_id = str(chat_id)
  
  if (chat_id not in initialize) or (initialize[chat_id] == False):
    collection = dbname['messages_'+chat_id]
    collection.insert_one({"role": "system", "content": "You are a helpful assistant."})
    initialize[chat_id] = True
  return
###########################---MAIN FUNCTION---##################################
@app.route("/{}".format(''), methods=["GET", "POST"])
def receive_message():
  if request.method == "POST":

    update = request.get_json()
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    send_chat_action(chat_id)
    respond_to_message(chat_id, message)

    return str(chat_id) + ": " + message
    
  else:
    return "Send a POST request to receive message!"
###########################################################################
def respond_to_message(chat_id, message):

  global initialize
  collection = dbname['messages_'+str(chat_id)]
  
  #clear the database
  if message == '/CLEAR' or message == '/clear':
    collection.delete_many({})
    send_message("Delete old conversation successfully!", chat_id)
    
    initialize[str(chat_id)] = False
    check_initDB(chat_id)
    return

  #Check if the database is not initialized
  check_initDB(chat_id)
  
  #Add user's message to database
  collection.insert_one({"role": "user", "content": message})
  
  #Resonse to message
  message_log = list(collection.find({}, {'_id': 0}))[-4:] #get 4 latest messages
  response = generate_response(message_log)
  send_message(response, chat_id)
  #send_with_simulation(response, chat_id)
  
  #Add chatGPT's response to database
  collection.insert_one({"role": "assistant", "content": response})
  return 
###########################################################################
def send_message(message, chat_id):
  
  requests.post(
    f"https://api.telegram.org/bot{bot_token}/sendMessage",
    json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "markdown"
    }
  )
  # msg = json.loads(response.content)['result']
  # message_id = msg['message_id']
  # return message_id
  
###########################################################################
def send_chat_action(chat_id):
  
  requests.post(
    f"https://api.telegram.org/bot{bot_token}/sendChatAction",
    json={
        "chat_id": chat_id,
        "action": "typing"
    }
  )
###########################################################################
def editMessageText(message, chat_id, message_id):
  requests.post(
    f"https://api.telegram.org/bot{bot_token}/editMessageText",
    json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": message,
        "parse_mode": "markdown"
    }
  )
###########################################################################
'''
def send_with_simulation(message, chat_id):

  message_id = send_message("Responding...", chat_id)
  message = re.findall(r'\S+|\n|\s',message)

  stack_message = ""
  for word in message:
    stack_message +=word
    editMessageText(stack_message, chat_id, message_id)
    #time.sleep(0.01)
'''
###########################################################################
def generate_response(message_log):
  
  try:
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages = message_log,
          max_tokens = 250,
          stop = None,
          temperature = 0.7
      )
    for choice in response.choices:
      if "text" in choice:
        return choice.text
            
    return response.choices[0].message.content
    
  except openai.error.InvalidRequestError as e:
    return str(e)[-55:]+"\nText '/CLEAR' or '/clear' to clean the old conversation in database!"
###########################################################################
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=8080, threaded = True)


# ChatGPT-and-Telegram
This an API connecting Telegram bot to ChatGPT (using Flask to create Application and Deployed on Pythonanywhere platfrom)
## Create a bot on Telegram
Open Telegram messenger, sign in to your account or create a new one.
1. Enter ***@Botfather*** in the search tab and choose this bot.
  - Click “Start” to activate BotFather bot.
  - In response, you receive a list of commands to manage bots.
2. Choose or type the *```/newbot```* command and send it.
3. Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”
  - After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.
4. Send the command *```/token```* and copy the bot's token.
## Set Webhook for the bot
We use webhook to receive incoming messages instead of making a while loop to wait
To set the webhook, copy this link and paste on the seaching bar
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_ENDPOINT>/<YOUR_SECRET_KEY>&allowed_updates=["message", "edited_message", "channel_post", "edited_channel_post", "callback_query"]
```
- ```<YOUR_BOT_TOKEN>```: this is your bot's token, you can get this after you create the bot and follow the above steps.
- ```<YOUR_ENDPOINT>```: the url of the place you hosting the bot.
- ```<YOUR_SECRET_KEY>```: place after the ```<YOUR_ENDPOINT>```, because your Flask app may have a lot of functions to host for supporting the bot but using a same endpoint. This secret key just to identify them.
## ChatGPT Model
We will use the "gpt-3.5-turbo" which is also called a chat completion and store the conversation in database using MongoDB.
An example API call looks as follows:
```
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
```
## Response format
An example API response looks as follows:
```
{
 'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
 'object': 'chat.completion',
 'created': 1677649420,
 'model': 'gpt-3.5-turbo',
 'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
 'choices': [
   {
    'message': {
      'role': 'assistant',
      'content': 'The 2020 World Series was played in Arlington, Texas at the Globe Life Field, which was the new home stadium for the Texas Rangers.'},
    'finish_reason': 'stop',
    'index': 0
   }
  ]
}
```
## How to create and connect to MongoDB
You can read the destriction on mongodb's official website
```
https://www.mongodb.com/docs/atlas/create-connect-deployments/
```


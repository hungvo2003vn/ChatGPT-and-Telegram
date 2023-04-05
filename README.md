# ChatGPT-and-Telegram
This an API connecting Telegram bot to ChatGPT (using Flask to create Application and Deployed on Pythonanywhere platfrom)
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


import os
import string

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
    token = os.environ["token"],
    signing_secret = os.environ['signing_secret']
)

with open("scientist.txt") as file:
    word_list = [line.lower().strip() for line in file.readlines()]

with open("keywords.txt") as file:
    keywords = [line.lower().strip() for line in file.readlines()]

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def react(message):
   client = app.client
   channel_id = message["channel"]
   timestamp = message["ts"]
   reaction_name = "half-life-2"

   client.reactions_add(
       channel=channel_id,
       timestamp=timestamp,
       name=reaction_name
   )

def keywords_in(message):
    cleaned_message = remove_punctuation(message["text"].lower())
    return any(keyword in cleaned_message.split() for keyword in keywords)

@app.use
def challenge_handler(req, resp, next):
    if req.body and req.body.get('challenge'):
        resp.body = req.body.get('challenge')
    else:
        next()

@app.message()
def reactor(message, say):

    if keywords_in(message) or message["text"].lower() in word_list:
        react(message)

@app.event("message") # stop throwing errors fgs
def handle_message_events(body, logger):
    logger.info(body)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["apptoken"]).start()
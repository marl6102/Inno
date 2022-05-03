import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAGjZCwCcxxgBAMVOZAT9BJm3wvy3ip5fmCTusDBZClATwlm7j8cXdyfghfnmP8qRv1dZBZAblqLo4ZCCBTI1VVS2ZCCaNZBua3jnGZBJMQeGAQSHUMecqrTDZAsjoEZA8iZBZCfuIoc9HInmC7qAjfFJ3l8pqJLLC2QHcWkK3snvdHgtf4gtSJSkBCqA'
VERIFY_TOKEN = 'Inno2022'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    user_message = message['message'].get('text')
                    #reply = _NLP.undertandMessage()
                    send_message(recipient_id, get_message())
    return "Message Processed"



def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["OO GWAPO TALAGA SIYA", "YES! TOO HANDSOME", "KYAH! PEMBARYA! SO FAFABLE", "DAMN! WHY SO HANDSOME BEBE BOY?"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
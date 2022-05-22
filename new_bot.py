from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button

app = Flask(__name__)

ACCESS_TOKEN = "EAAGjZCwCcxxgBAOXvgOkwL4FY9B1518QDXAtzJPv8Si7mJGtGFyDPJ6Bnb62XTlyeZAhgFebVHwzhOPYY8DuKF5SrB5zGvgeecGYmcsPdMOZBO8i0MqPYSvzgNqSETMSJclWtFZCvZAIQUx63IFzUvN4ezO5VAOu1AWfNG6AMUJfK3ltQDQFZA"
VERIFY_TOKEN = "Inno2022"
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                recipient_id = x['sender']['id']
                if x.get('message'):
                    
                    if x['message'].get('text'):
                        message = x['message']['text']

                        buttons = []
                        button = Button(title='BSCS', type='postback', payload='BSCS')
                        buttons.append(button)
                        button = Button(title='BSIT', type='postback', payload='BSIT')
                        buttons.append(button)
                        button = Button(title='BSIS', type='postback', payload='BSIS')
                        buttons.append(button)    
                        text = 'Select topic'
                        result = bot.send_button_message(recipient_id, text, buttons)

                        
                elif x.get('postback'):
                    payload = x['postback'].get('payload')
                    '''print(payload)
                    bot.send_text_message(recipient_id, payload)'''
                    reply_responses(recipient_id)
                else:
                    pass
        return "Success"

def reply_responses(recipient_id):
    buttons = []
    button = Button(title='BSCS Instructors', type='postback', payload='BSCS Instructors')
    buttons.append(button)
    button = Button(title='BSIT Instructors', type='postback', payload='BSIT Instructors')
    buttons.append(button)
    button = Button(title='BSIS Instructors', type='postback', payload='BSIS Instructors')
    buttons.append(button)    
    text = 'Select topic'
    result = bot.send_button_message(recipient_id, text, buttons)


if __name__ == "__main__":
    app.run()
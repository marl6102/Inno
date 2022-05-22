from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
import pyodbc

app = Flask(__name__)

ACCESS_TOKEN = "EAAGjZCwCcxxgBAJrPuObjYH3zWP4ZBf097ZBTYahHb4n0xc2Na5Pctsbk4HcnZB3kFykkYtKzLQhqyXuM9ZB9lVawXaGRgTWjxMukQ6MZAaAVM7Www4oJVGahnVTCVBCvRAytXyB3ZAZCEhq14pvG0vvmThtjjN3uaRkEWIKnoOEaEahZCMtJcauf"
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
                        print(message)

                        main_menu(recipient_id)
                        
                elif x.get('postback'):
                    payload = x['postback'].get('payload')
                    pay = x['postback'].get('title')
                    print('===========')
                    print('Payload: ' + pay)
                    print('Len:')
                    print(len(pay))
                    print('===========')

                    if len(pay) > 11:
                        message = get_response(payload)
                        bot.send_text_message(recipient_id, message)
                        main_menu(recipient_id)

                    else:
                        menus = getMenu(payload)
                        buttons = []
                        for mns in menus:
                            button = Button(title=mns, type='postback', payload=mns)
                            buttons.append(button)
                        print(menus)
                        bot.send_button_message(recipient_id, 'Select topic', buttons)
                else:
                    pass
        return "Success"

def main_menu(recipient_id):
    keywords = getKeywords()
    buttons = []
    for keys in keywords:
        button = Button(title=keys, type='postback', payload=keys)
        buttons.append(button)

    bot.send_button_message(recipient_id, 'Select topic', buttons)

def getKeywords():
    #database details
    server = 'localhost' 
    database = 'INNO'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')

    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Keywords')
    row = cursor.fetchall()
    tags = []

    for i in row:
        data = i[1]
        tags.append(data)

    #print(tags)
    return tags

def getMenu(payload):
    #database details
    server = 'localhost' 
    database = 'INNO'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')

    cursor = cnxn.cursor()
    cnstring = "SELECT * FROM Responses WHERE Tag LIKE '" + payload + "%';"
    cursor.execute(cnstring)
    row = cursor.fetchall()
    tags = []

    for i in row:
        data = i[1]
        tags.append(data)

    #print(tags)
    return tags

def get_response(question):
    #database details
    server = 'localhost' 
    database = 'INNO'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')

    cursor = cnxn.cursor()
    cnstring = "SELECT * FROM Responses WHERE Question LIKE '" + question + "%';"
    cursor.execute(cnstring)
    row = cursor.fetchall()
    print(row[0][2])
    return row[0][2]

if __name__ == "__main__":
    app.run()
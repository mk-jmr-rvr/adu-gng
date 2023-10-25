from flask import Flask, render_template, request
import random
import json
import os
import urllib.parse
from botConfig import myBotName, chatBG, botAvatar, useGoogle, confidenceLevel
from botRespond import getResponse
from dateTime import getTime, getDate

application = Flask(__name)

chatbotName = myBotName
print("Bot Name set to: " + chatbotName)
print("Background is " + chatBG)
print("Avatar is " + botAvatar)
print("Confidence level set to " + str(confidenceLevel))

# Create Log file
botLog = os.path.abspath('BotLog.json')

def tryGoogle(myQuery):
    myQuery = myQuery.replace("'", "%27")
    showQuery = urllib.parse.unquote(myQuery)
    return "<br><br>You can try this from my friend Google: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + showQuery + "</a>"

@application.route("/")
def home():
    return render_template("index.html", botName=chatbotName, chatBG=chatBG, botAvatar=botAvatar)

@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(getResponse(userText))

    if botReply == "IDKresponse":
        botReply = str(getResponse('IDKnull'))  # Send the I don't know code back to the DB
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())

    # Log to JSON file
    print("Logging to JSON file now")
    log_entry = {"userText": userText, "botReply": botReply}
    with open(botLog, 'a') as logFile:
        logFile.write(json.dumps(log_entry) + '\n')

    return botReply

if __name__ == "__main":
    # application.run()
    application.run(host='0.0.0.0', port=80)

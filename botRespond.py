from botConfig import confidenceLevel
from difflib import SequenceMatcher
import urllib.parse
import json
import random

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getResponse(sendMsg):
    #return "You said: " + sendMsg
    sendMsg = urllib.parse.unquote(sendMsg)
    # Loop through JSON knowledge file. If a question is equal to or greater than the confidence level, add it to a list of possible responses. Then return a random response.
    lineCount = 0
    successCount = 0
    exactCount = 0
    comeBacks = []
    exactReply = []
    exactMatch = 0.9

    with open('data/chatbot.json', 'r') as json_file:
        data = json.load(json_file)

    for entry in data:
        lineCount += 1
        userText = entry.get('userText')
        botReply = entry.get('botReply')
        if not userText or not botReply:
            print("WARNING: I had to skip entry #" + str(lineCount) + " due to missing data.")
        else:
            checkMatch = similar(sendMsg, userText)
            if checkMatch >= exactMatch:
                exactCount += 1
                exactReply.append(botReply)
                print("Likely match: " + userText)
                print("Match is: " + str(checkMatch))
            elif checkMatch >= confidenceLevel:
                successCount += 1
                comeBacks.append(botReply)
                print("Possible match: " + userText)
                print("Match is: " + str(checkMatch))

    if exactCount >= 1:
        botResponsePick = random.choice(exactReply)
    elif successCount >= 1:
        botResponsePick = random.choice(comeBacks)
    else:
        botResponsePick = "IDKresponse"
    
    return botResponsePick

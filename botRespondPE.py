from botConfig import confidenceLevel
from difflib import SequenceMatcher
import urllib.parse
import json
import random
import os

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getResponse(sendMsg):
    sendMsg = urllib.parse.unquote(sendMsg)
    lineCount = 0
    successCount = 0
    exactCount = 0
    comeBacks = []
    exactReply = []
    exactMatch = 0.9

    botBrain = os.path.abspath('mybot/data/chatbot.json')

    with open(botBrain, 'r') as g:
        data = json.load(g)

    for entry in data:
        lineCount += 1
        if "userText" not in entry or "botReply" not in entry:
            print("WARNING: Entry #" + str(lineCount) + " is missing data.")
            continue

        userText = entry["userText"]
        botReply = entry["botReply"]
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

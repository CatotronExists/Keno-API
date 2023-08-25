### KENO DATAVIS ###
## MAIN.PY ##
# Modules #
from keno import keno_app
import time
import datetime
from datetime import timedelta
import sys
import pymongo
import certifi
import json
#         #

# Files #
from Config import configVersion, configCheck, countdown, cooldown
from Api import GetAPI, apiVersion, GetJackpots
from WinList import winListVersion, ClassicWinlists, MegaMillionWinlists
from Setup import setupVersion
#       #

# Terminal Colors #
import os
os.system("")
CLEAR = '\33[0m'
CGREEN = '\33[92m'
CBLUE = '\33[34m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CBEIGE = '\33[36m'
CBOLD = '\033[1m'
#                #

# Vars #
mainVersion = "v0.4.d-3"
path = './Credentials.json'
file = os.path.exists(path)
ca = certifi.where()
#      #

def PrintMainUI(drawNumbers): # Build Main UI
    finalNumbers = []
    for i in drawNumbers: # Highlights matched numbers
        i = CGREEN + str(i) + CLEAR
        finalNumbers.append(i)
    finalNumbers = ", ".join(map(str, finalNumbers))

    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("Game Number: " + CBOLD + str(gameNumber) + CLEAR + "  |  Game Started at: " + CBOLD + str(startTime) + CLEAR + " UTC  |  Data Pulled at: " + CBOLD + str(currentTime) + CLEAR + " UTC")
    print("Numbers Drawn: " + str(finalNumbers))
    print("Multiplier: " + str(bonus))
    print("Heads/Tails Result: " + str(HTResultDisplay) + CLEAR + "  |  " + CRED + "Heads: " + str(HResult) + CBLUE + "  Tails: " + str(TResult) + CLEAR)
    print(CBLUE + "---------------------------------------------------------------------" + CLEAR) 

    if databasing == True:
        # Create string version of everything
        drawString = drawNumbers = ", ".join(map(str, drawNumbers))
        gameNumberString = str(gameNumber)
        multiplierString = str(multiplier)
        gameDataDB.insert_one(
            {"timestamp" : startTime,
            "gameNumber" : gameNumberString,
            "drawNumbers" : drawString,
            "multiplier" : multiplierString,
            "headTailResult" : HTResult},
        )

def GetData(): # Sorts API Data
    global currentTime, startTime, gameNumber, bonus, HTResultDisplay, TResult, HResult, multiplier, HTResult, drawNumbers
    liveData = 0
    liveData = GetAPI(liveData)
    gameNumber = liveData["game_number"] # Game Number
    drawNumbers = liveData["draw_numbers"] # Drawn Numbers
    drawNumbers.sort(key = lambda x: x, reverse = False)
    startTime = liveData["started_at"] # Game Start Time
    startTime = datetime.datetime.strptime(startTime.split('.')[0], '%Y-%m-%d %H:%M:%S')
    currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f') # Current Time
    currentTime = datetime.datetime.strptime(currentTime.split('.')[0],'%Y-%m-%d %H:%M:%S')
    bonus = liveData["bonus"] # Bonus and Multiplier 
    if bonus == "reg":
        multiplier = 1
        bonus = CRED + "reg" + CLEAR
    elif bonus == "x2":
        multiplier = 2
        bonus = CYELLOW + "x2" + CLEAR
    elif bonus == "x3":
        multiplier = 3
        bonus = CGREEN + "x3" + CLEAR
    elif bonus == "x4":
        multiplier = 4
        bonus = CBOLD + CGREEN + "x4" + CLEAR
    elif bonus == "x5":
        multiplier = 5
        bonus = CBOLD + CYELLOW + "x5" + CLEAR
    elif bonus == "x10":
        multiplier = 10
        bonus = CBOLD + CBLUE + "x10" + CLEAR
    HTResult = liveData["result"] # H / T data 
    HTResult = HTResult.capitalize()
    if HTResult == "Tails": HTResultDisplay = CBOLD + CBLUE + "Tails" + CLEAR
    elif HTResult == "Heads": HTResultDisplay = CBOLD + CRED + "Heads" + CLEAR
    elif HTResult == "Evens": HTResultDisplay = CBOLD + CBEIGE + "Evens" + CLEAR
    HResult = liveData["heads"] # Number of head numbers
    TResult = liveData["tails"] # Number of tail numbers

def Wait(currentTime, startTime, cooldown): # Cooldown between calls
    if cooldown == "Auto": # Calculate auto cooldown
        timeDelta = currentTime - startTime
        cooldown = (160 - (int(timeDelta.total_seconds()))) + 10
    else: cooldown = cooldown # Use Config 
    if countdown == "True":
        for i in reversed(range(cooldown + 1)): 
            if i == 0: # if countdown is 0 -> show 0 then clear line
                sys.stdout.write("\r" + CBEIGE + "Next Request in: " + str(i) + " seconds      " + CLEAR)
                sys.stdout.flush()    
                time.sleep(1)
                sys.stdout.write("\r")
                sys.stdout.flush()
            else:    
                sys.stdout.write("\r" + CBEIGE + "Next Request in: " + str(i) + " seconds      " + CLEAR)
                sys.stdout.flush()
                time.sleep(1)
    elif countdown == "Manual": input("")
    else: time.sleep(cooldown)

def Debug(mainVersion, configVersion, apiVersion, winListVersion, setupVersion):
    print("/// Debug Menu ///")
    print("Main - " + mainVersion + "\nConfig - " + configVersion + "\nApi - " + apiVersion + "\nWinList - " + winListVersion + "\nSetup - " + setupVersion)

if configCheck == True: 
    configErrors = active = 0

    if type(cooldown) is int:
        cooldown = int(cooldown)
        if cooldown < 140:
            print(CRED + "cooldown is set to an invaild value {" + str(cooldown) +"}, Check config.py for valid values" + CLEAR)
            configErrors += 1 
    else:  
        if cooldown != "Auto":
            print(CRED + "cooldown is set to an invaild value {" + str(cooldown) +"}, Check config.py for valid values" + CLEAR)
            configErrors += 1 

    if countdown == "True" or countdown == "False" or countdown == "Manual": pass
    else: 
        print(CRED + "countdown is set to an invaild value {" + str(countdown) +"}, Check config.py for valid values" + CLEAR)
        configErrors += 1 
    
    if configErrors != 0: input(CRED + str(configErrors) + " Config Errors Found" + CLEAR)
    else:
        active = True
        print(CYELLOW + "Getting First Time API Data..." + CLEAR)
        GetData()
else:
    active = True
    print(CYELLOW + "Getting First Time API Data..." + CLEAR)
    GetData()

while active == True:
    while configErrors == 0:
        mainChoice = 0
        while mainChoice == 0:
            print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
            print(CBOLD + "1. " + CLEAR + "Live Game Viewer (With Databasing)")
            print(CBOLD + "2. " + CLEAR + "Live Game Viewer (Without Databasing)")
            mainChoice = input("--->> ")
            if mainChoice.isnumeric():
                mainChoice = int(mainChoice)
                if mainChoice == 1: print("Opening" + CYELLOW + CBOLD + " Live Game Viewer: Database Edition" + CLEAR)
                elif mainChoice == 2: print("Opening" + CYELLOW + CBOLD + " Live Game Viewer" + CLEAR)
                else: 
                    mainChoice = 0
                    print(CRED + "Invaild Option" + CLEAR)
            elif mainChoice == "debug": Debug(mainVersion, configVersion, apiVersion, winListVersion, setupVersion)
            else:
                mainChoice = 0
                print(CRED + "Invaild Option" + CLEAR)
        
        time.sleep(1)
        print("\n"*4)

        if mainChoice == 1: # Databasing
            databasing = True
            if file == True:
                with open('Credentials.json') as jsonFile:
                    data = json.load(jsonFile)
                    credentials = "mongodb+srv://" + data["user"] + ":" + data["password"] + data["restOfString"]
                    active = True
                    client = pymongo.MongoClient(credentials, tlsCAFile=ca)
                    db = client["kenoGameData"] # defines db (database)
                    gameDataDB = db["GameData"] # defines GameData (GameData Storage)
            else: 
                databasing = False
                active = False
                print(CRED + "Setup has not been completed, Run Setup.py" + CLEAR + "\nRunning without Databasing Enabled in 3 seconds")
                time.sleep(3)
        elif mainChoice == 2: databasing = False # No Databasing
        while True:
            PrintMainUI(drawNumbers)
            Wait(currentTime, startTime, cooldown)
            GetData()
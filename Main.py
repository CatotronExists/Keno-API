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
from Config import configCheck, countdown, cooldown, app, display
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
version = "v0.4.d-7"
ca = certifi.where()
#      #

def GetAPI(liveData):
    lastGameNumber = "n/a"
    while liveData == 0:
        try: 
            time.sleep(0.1)
            liveData = app.live_draw()
            gameNumber = liveData["game_number"]
            if lastGameNumber == gameNumber: # in case the same game is called twice, try again after 10 sec
                print(CRED + "Already Fetched Game: " + str(gameNumber) + " Retrying in 10 seconds..." + CLEAR)
                liveData = 0
                time.sleep(10)
            lastGameNumber == gameNumber
            return liveData
        except Exception as e: print(CRED + str(e) + CLEAR)

def PrintMainUI(drawNumbers): # Build Main UI
    if display == True:
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
    else: pass
    # Create string version of everything
    drawString = drawNumbers = ", ".join(map(str, drawNumbers))
    gameNumberString = str(gameNumber)
    multiplierString = str(multiplier)
    startTimeString = str(startTime)
    gameDataDB.insert_one(
        {"timestamp" : startTime,
        "gameTime" : startTimeString,
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
        cooldown = (160 - (int(timeDelta.total_seconds()))) + 5
    else: cooldown = cooldown # Use Config 
    if countdown == True:
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
    else: time.sleep(cooldown)

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

    if countdown == True or countdown == False: pass
    else: 
        print(CRED + "countdown is set to an invaild value {" + str(countdown) +"}, Check config.py for valid values" + CLEAR)
        configErrors += 1 
    
    if display == True or display == False: pass
    else: 
        print(CRED + "display is set to an invaild value {" + str(display) +"}, Check config.py for valid values" + CLEAR)
        configErrors += 1 

    if configErrors != 0: input(CRED + str(configErrors) + " Config Errors Found" + CLEAR)
    else: active = True

else: active = True

while active == True:
    error = False
    print(CBOLD + CBLUE + "Keno Tracker              "+ version +"          " + CLEAR)
    time.sleep(2)
    print(CYELLOW + "Checking Setup Status...")
    time.sleep(0.5)
    path = './Credentials.json'
    file = os.path.exists(path)
    if error != True: # Find Credentials
        if file == True:
            with open('Credentials.json') as jsonFile:
                data = json.load(jsonFile)
                try: 
                    credentials = "mongodb+srv://" + data["user"] + ":" + data["password"] + data["restOfString"]
                    client = pymongo.MongoClient(credentials, tlsCAFile=ca)
                    db = client["kenoGameData"] # defines db (database)
                    gameDataDB = db["GameData"] # defines GameData (GameData Storage)
                    print(CGREEN + "         Found Credentials.json" + CLEAR)
                except Exception as e: 
                    error = True
                    print(CRED +  "         Credentials.json is corrupt, delete it and run setup again!" + CLEAR)
                    print(CRED + "         The following field(s) are missing, " + str(e) + CLEAR)
                    input("")
        else: 
            error = True
            print(CRED + "Setup has not been completed/Credentials.json could not be found, Run Setup.py to resolve" + CLEAR)
            input("")        

    if error != True: # Test Credentials
        print(CYELLOW + "Testing Connection to MongoDB..." + CLEAR)
        try: 
            client.db.command('ping')
            print(CGREEN + "         Successfully connected to MongoDB" + CLEAR)
        except Exception as e:
            error = True
            print(CRED + e + CLEAR)
            print(CRED +  "         A connection to MongoDB could not be established, check if your credentials are correct!" + CLEAR)
            input("")
    
    if error != True:
        print(CGREEN + CBOLD + "Startup Complete..." + CLEAR)
        time.sleep(2.5)
        print("\n"*4)
        while True:
            GetData()
            PrintMainUI(drawNumbers)
            Wait(currentTime, startTime, cooldown)
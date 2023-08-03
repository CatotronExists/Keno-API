### KENO DATAVIS ###
## MAIN.PY ##
# Modules #
from keno import keno_app
import time
import datetime
from datetime import timedelta
import sys
import random
#         #

# Files #
from Config import configVersion, configCheck, countdown, cooldown
from Api import GetAPI, apiVersion, GetJackpots
from WinList import winListVersion, ClassicWinlists, MegaMillionWinlists
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
mainVersion = "Legacy-08/2023-1"
currency = "$" # $ - normal currency, κ - Koins
vaildSpots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40]
picked = []
totalWin = 0
#      #

def PrintMainUI(drawNumbers): # Build Main UI
    global picked
    finalNumbers = []
    numbersMatched = 0
    for i in drawNumbers: # Highlights matched numbers
        if i in picked:
            i = CYELLOW + str(i) + CLEAR
            numbersMatched += 1
            finalNumbers.append(i)
        else:
            i = CGREEN + str(i) + CLEAR
            finalNumbers.append(i)
    finalNumbers = ", ".join(map(str, finalNumbers))

    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("Game Number: " + CBOLD + str(gameNumber) + CLEAR + "  |  Game Started at: " + CBOLD + str(startTime) + CLEAR + " UTC  |  Data Pulled at: " + CBOLD + str(currentTime) + CLEAR + " UTC")
    print("Numbers Drawn: " + str(finalNumbers))
    print("Multiplier: " + str(bonus))
    print("Heads/Tails Result: " + str(HTResultDisplay) + CLEAR + "  |  " + CRED + "Heads: " + str(HResult) + CBLUE + "  Tails: " + str(TResult) + CLEAR)

    if monitor == True:
        CalclateWin(mode, numbersMatched)
        if mode == "Classic" or mode == "Mega Million":
            GetJackpots()
            if lastGame == True: print("Result: " + CBOLD + str(numbersMatched) + CLEAR + " Numbers Matched  |  Won: " + str(winDisplay) + "    " + CYELLOW  + CBOLD + "LAST GAME " + CLEAR)
            else: print("Result: " + CBOLD + str(numbersMatched) + CLEAR + " Numbers Matched  |  Won: " + str(winDisplay))
        else:
            if lastGame == True: print("Result: Picked " + str(HTChoice) + "  |  Won: " + str(winDisplay) + "    " + CYELLOW  + CBOLD + "LAST GAME " + CLEAR)
            else: print("Result: Picked " + str(HTChoice) + "  |  Won: " + str(winDisplay))

    print(CBLUE + "---------------------------------------------------------------------" + CLEAR)

def CalclateWin(mode, numbersMatched):
    global winDisplay, totalWin
    if mode == "Classic" or mode == "Mega Million":
        if mode == "Classic": win = ClassicWinlists[spot][numbersMatched] * bet
        elif mode == "Mega Million": win = MegaMillionWinlists[spot][numbersMatched] * bet

        if multiStatus == True: win = win*multiplier # Calculate Bonus (If on)

        if win > 0: winDisplay = (CGREEN + str(currency) + str(win) + CLEAR)
        else: winDisplay = (CRED + str(currency) + str(win) + CLEAR)
    
    elif mode == "Heads / Tails":
        if HTResult == HTChoice:
            if HTResult == "Heads" or HTResult == "Tails": 
                win = bet*2
                winDisplay = (CGREEN + str(currency) + str(win) + CLEAR) 
            elif HTResult == "Evens": 
                win = bet*4
                winDisplay = (CGREEN + str(currency) + str(win) + CLEAR)
        else: 
            win = 0
            winDisplay = (CRED + str(currency) + str(win) + CLEAR)
    totalWin += win   

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
        cooldown = 160 - (int(timeDelta.total_seconds()))
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

def ShowTicket():
    print(CBLUE + "-----------------------------------" + CLEAR)  
    print(CBOLD + "Ticket information" + CLEAR)
    print(mode + " Keno")
    print("Total Numbers: " + str(spot))
    print("Picked Numbers: " + str(picked))
    print("Ending Game: " + str(finalGame))
    if mode == "Classic": print("Bonus Enabled: " + str(multiStatus))
    print("Bet per game: " + str(currency) + str(int(bet/totalGames)))
    input("Press [Enter] to start\n")

def EndScreen():
    print(CBOLD + CBLUE + "Keno Tracker" + CLEAR)
    print(CBOLD + "Keno " + mode + " Ticket Result" + CLEAR)
    if mode == "Classic" or mode == "Mega Million":
        if multiStatus == True: print("Playing Spot " + str(spot) + ", with Bonus Enabled")
        else: print("Playing Spot " + str(spot))
        print("Picked Numbers: " + str(picked))
        print("Winnings: " + str(currency) + str(totalWin))
        print("Games: " + CBOLD + str(startGame) + CLEAR + " - " + CBOLD + str(finalGame) + CLEAR + " Total Games: " + str(totalGames)) 
    elif mode == "Heads / Tails":
        print("Predicted Outcome: " + str(HTChoice))
        print("Outcome: " + str(HTResultDisplay))
        print("Winnings: " + str(currency) + str(totalWin))
        print("Game: " + str(finalGame))
    print(CBLUE + "---------------------------------------------------------------------" + CLEAR)
            
def Debug(mainVersion, configVersion, apiVersion, winListVersion):
    print("/// Debug Menu ///")
    print("Main - " + mainVersion + "\nConfig - " + configVersion + "\nApi - " + apiVersion + "\nWinList - " + winListVersion)

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
    
    if configErrors != 0:
        print(CRED + str(configErrors) + " Config Errors Found" + CLEAR)
    else:
        active = True
        print(CYELLOW + "Getting First Time API Data..." + CLEAR)
        GetData()
        GetJackpots()
else:
    active = True
    print(CYELLOW + "Getting First Time API Data..." + CLEAR)
    GetData()
    GetJackpots()

while active == True:
    mainChoice = secondaryChoice = pickMode = HTChoice = bet = spot = pick = win = 0
    finalGame = startGame = multiStatus = -1
    inMenus = True
    monitor = lastGame = False
    while mainChoice == 0:
        print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
        print(CBOLD + "1. " + CLEAR + "Live Game Viewer")
        print(CBOLD + "2. " + CLEAR + "Bet Simulator")
        print(CBOLD + "3. " + CLEAR + "Bet Monitor")
        print("Currently Game " + str(gameNumber))
        mainChoice = input("--->> ")
        if mainChoice.isnumeric():
            mainChoice = int(mainChoice)
            if mainChoice == 1: print("Opening" + CYELLOW + CBOLD + " Live Game Viewer" + CLEAR)
            elif mainChoice == 2: print("Opening" + CYELLOW + CBOLD + " Bet Simulator" + CLEAR)
            elif mainChoice == 3: print("Opening" + CYELLOW + CBOLD + " Bet Monitor" + CLEAR)
            else: 
                mainChoice = 0
                print(CRED + "Invaild Option" + CLEAR)
        elif mainChoice == "debug": Debug(mainVersion, configVersion, apiVersion, winListVersion)
        else:
            mainChoice = 0
            print(CRED + "Invaild Option" + CLEAR)
    
    time.sleep(1)
    print("\n"*4)
    if mainChoice == 1: inMenus = False # Live Game Viewer
    if inMenus == True:
        monitor = True 
        while mainChoice == 2 or mainChoice == 3: # Bet Simulator / Monitor
            if mainChoice == 2: secondary = "Simulator"
            else: secondary = "Monitor"
            print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
            print(CBOLD + "Bet " + secondary + CLEAR)
            while secondaryChoice == 0:
                print("Select Mode\n" + CBOLD + "1. " + CLEAR + "Classic\n" + CBOLD + "2. " + CLEAR + "Mega Millions\n" + CBOLD + "3. " + CLEAR + "Heads / Tails")
                secondaryChoice = input("--->> ")
                if secondaryChoice.isnumeric():
                    secondaryChoice = int(secondaryChoice)
                    if secondaryChoice == 1: mode = "Classic"
                    elif secondaryChoice == 2: mode = "Mega Million"
                    elif secondaryChoice == 3: mode = "Heads / Tails"
                    else: 
                        secondaryChoice = 0
                        print(CRED + "Invaild Option" + CLEAR)
                else: 
                    secondaryChoice = 0
                    print(CRED + "Invaild Option" + CLEAR)
            
            print("Opening " + CBOLD + mode + " Keno " + secondary + CLEAR)

            if mode == "Heads / Tails": # H/T Bet Simulator / Monitor
                print(CBOLD + CBLUE + "\nKeno Tracker                  " + CLEAR)
                print(CBOLD + mode + " Keno " + secondary + CLEAR)  
                if secondary == "Simulator":
                    currency = "κ"
                    while pickMode == 0:
                        pickMode = input("How will you pick the outcome?\n1. Kwikpik\n2. Manual\n--->> ")
                        if pickMode.isnumeric():
                            pickMode = int(pickMode)
                            if pickMode == 1: print("Kwikpik Selected")
                            elif pickMode == 2: print("Manual Selected")
                            else:
                                pickMode = 0
                                print(CRED + "Invaild Option" + CLEAR)
                        else:
                            pickMode = 0
                            print(CRED + "Invaild Option" + CLEAR)

                if pickMode == 1: # Kwikpik
                    print("Picking...")
                    time.sleep(1)
                    HTChoice = random.randint(1,5)
                    if HTChoice == 1 or HTChoice == 2: HTChoice = "Heads" # 1-2
                    elif HTChoice == 3 or HTChoice == 4: HTChoice = "Tails" # 3-4
                    else: HTChoice = "Evens" # 5
                    print("Auto Picked: " + CBOLD + HTChoice + CLEAR)
                elif pickMode == 2: # Manual
                    while HTChoice == 0: 
                        HTChoice = input("What outcome have you picked? (heads/tails/evens)\n--->> ")
                        if HTChoice == "heads" or HTChoice == "tails" or HTChoice == "evens":
                            HTChoice.capitalize()
                            print("You have chosen " + CBOLD + HTChoice + CLEAR)
                        else: 
                            HTChoice = 0
                            print(CRED + "Invaild Option" + CLEAR)

                while bet == 0:
                    bet = input("What is the bet amount\n" + currency)
                    if bet.isnumeric(): bet = int(bet)
                    else:
                        bet = 0
                        print(CRED + "Invaild Option" + CLEAR)
                
                while finalGame == -1:
                    finalGame = input("What game is this bet for/n--->> ")
                    if finalGame.isnumeric():
                        finalGame = int(finalGame)
                        if finalGame in range(0,999 + 1): ShowTicket()
                        else:                            
                            finalGame = -1
                            print(CRED + "Invaild Option" + CLEAR) 
                    else:
                        finalGame = -1
                        print(CRED + "Invaild Option" + CLEAR) 

            elif mode == "Classic" or mode == "Mega Million": # Keno Bet Monitor/Simulator
                print(CBOLD + CBLUE + "\nKeno Tracker                  " + CLEAR)
                print(CBOLD + mode + " Keno " + secondary + CLEAR)
                if secondary == "Simulator":
                    currency = "κ"
                    while pickMode == 0:
                        pickMode = input("How will you pick your numbers\n1. Kwikpik\n2. Manual\n--->> ")
                        if pickMode.isnumeric():
                            pickMode = int(pickMode)
                            if pickMode == 1: print("Kwikpik Selected")
                            elif pickMode == 2: print("Manual Selected")
                            else:
                                pickMode = 0
                                print(CRED + "Invaild Option" + CLEAR)
                        else:
                            pickMode = 0
                            print(CRED + "Invaild Option" + CLEAR)
                elif secondary == "Monitor": currency = "$"

                while spot == 0:
                    if pickMode == 1: spot = input("\nHow many numbers do you wish to play\n--->> ")
                    else: spot = input("\nHow many numbers have been picked\n--->> ")
                    if spot.isnumeric():
                        spot = int(spot)
                        if spot not in vaildSpots:
                            spot = 0
                            print(CRED + "Invaild Option" + CLEAR)
                    else: 
                        spot = 0
                        print(CRED + "Invaild Option" + CLEAR)
                print("Playing " + CBOLD + str(spot) + CLEAR + " Numbers")

                if pickMode == 1: picked = random.sample(range(1,80+1), spot) # Kwikpik 
                elif pickMode == 2: 
                    picked = pickedDisplay = []
                    print("\nInput your picks, type in one number per line")
                    for i in range(spot):
                        pick = 0
                        while pick == 0:
                            pick = input("")
                            if pick.isnumeric():
                                pick = int(pick)
                                if pick in picked:
                                    print(CRED + "You have already chosen " + str(pick) + CLEAR)
                                    pick = 0
                                elif pick not in range (1,80+1):
                                    pick = 0
                                    print(CRED + "Invaild Option" + CLEAR)
                            else:
                                pick = 0
                                print(CRED + "Invaild Option" + CLEAR)
                        picked.append(pick)
                picked.sort(key = lambda x: x, reverse = False)
                pickedDisplay = picked
                pickedDisplay = ", ".join(map(str, pickedDisplay))
                print("---------------------------\nNumbers Picked: " + str(pickedDisplay))

                while startGame == -1: 
                    startGame = input("\nWhat is the first game on the ticket\n--->> ")
                    if startGame.isnumeric():
                        startGame = int(startGame)
                        if startGame not in range(0,999 + 1): # must be in 000-999
                            startGame = -1
                            print(CRED + "Invaild Option" + CLEAR)     
                    else:
                        startGame = -1
                        print(CRED + "Invaild Option" + CLEAR) 
                print("Starting game is: " + CBOLD + str(startGame) + CLEAR)

                while finalGame == -1:
                    finalGame = input("\nWhat is the final game on the ticket\n--->> ")
                    if finalGame.isnumeric():
                        finalGame = int(finalGame)
                        if finalGame not in range(0,999 + 1): # must be in 000-999
                            finalGame = -1
                            print(CRED + "Invaild Option" + CLEAR)  
                        elif finalGame == startGame:
                            finalGame = -1
                            print(CRED + "Invaild Option" + CLEAR)  
                    else:
                        finalGame = -1
                        print(CRED + "Invaild Option" + CLEAR) 
                print("Final game is: " + CBOLD + str(finalGame) + CLEAR)

                totalGames = startGame - finalGame
                if totalGames < 0: # if games selected 'wrap around' e.g 989 to 4
                    totalGames = finalGame - startGame
                
                if mode == "Classic":
                    while multiStatus == -1:
                        multiStatus = input("\nIs Keno Bonus on? (y/n)\n--->> ")
                        if multiStatus == "y": multiStatus = True
                        elif multiStatus == "n": multiStatus = False
                        else:
                            multiStatus = -1
                            print(CRED + "Invaild Option" + CLEAR) 
                else: multiStatus = False
                
                while bet == 0:
                    bet = input("\nWhat is the bet amount\nIf you have bonus on, half the bet amount shown on your ticket\n" + str(currency))
                    if bet.isnumeric():
                        bet = int(bet)
                        if bet == 0 or bet < 0:
                            bet = 0
                            print(CRED + "Invaild Option" + CLEAR)
                    else:
                        bet = 0
                        print(CRED + "Invaild Option" + CLEAR)
                
                ShowTicket()
                inMenus = False
                mainChoice = 4

    while inMenus == False:
        if finalGame == gameNumber:
            lastGame = True
            GetData()
            PrintMainUI(drawNumbers)
            input(CYELLOW + "Bet Complete! " + CLEAR +"\nPress " + CBOLD + "[Enter]" + CLEAR + " to see bet results")
            EndScreen()
        else: 
            GetData()
            PrintMainUI(drawNumbers)
            Wait(currentTime, startTime, cooldown)
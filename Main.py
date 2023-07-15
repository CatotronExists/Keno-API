from keno import keno_app
from Api import getAPI, ApiVersion
from Config import cooldown, countdown, ConfigVersion
from WinList import *
import time
import datetime
import sys

### FIND HOW OFTEN A GAME STARTS (seems to be every 2:40 ~160sec)
### GET THE API REQUEST ~10 SECONDS AFTER GAME START

### TODO Before v0.2
# add bet amount per game / outcome to bet monitor (c/mm/ht)
# complete functionality of first game / last game + Last game alert
# total winnings screen after last game
# FIX same game cooldown 
# Start the countdown after the API request not after all data displayed (the timing is slowly thrown off overtime)
# SPEED UP program using threading, (One thread for each part of the main screen)

### Terminal Colors
import os
os.system("")
CLEAR = '\33[0m'
CGREEN = '\33[92m'
CBLUE = '\33[34m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CBEIGE = '\33[36m'
CBOLD = '\033[1m'

MainVersion = "v0.1.d-23"
menu_choice = 0
monitor_menu_choice = 0
total_numbers = 0
numbers_picked = []
m_vaild = [1, 2, 3, "debug"] # Menu vaild choices
mm_vaild = [1, 2, 3] # Monitor Menu vaild choices
km_vaild = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40] # Keno Monitor (vaild number of chosen numbers)
numbers_picked = []
numbers_picked_display = []
final_game = 0
multi_status = -1
bet_amount = 1 # temp solution for h/t

# TESTING TIME BETWEEN GAMES
last_start_time = datetime.datetime.utcnow()

def PrintMainUI(): ### Build Terminal Output
    global last_start_time # TESTING TIME BETWEEN GAMES
    # Checks all numbers, if not in a bet monitor mode all numbers will be green as there is no matching
    final_numbers = []
    numbers_matched = 0
    for i in draw_numbers:
        if i in numbers_picked: # if its a picked number -> turn yellow
            i = CYELLOW + str(i) + CLEAR
            numbers_matched = numbers_matched + 1
            final_numbers.append(i)
        else: # if its not a picked number -> turn green
            i = CGREEN + str(i) + CLEAR
            final_numbers.append(i)
    final_numbers = ", ".join(map(str, final_numbers))

    ### Testing Game Timing
    differnce = start_time - last_start_time

    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("Game Number: " + CBOLD + str(game_number) + CLEAR + "  |  Game Started at: " + CBOLD + str(start_time) + CLEAR + " UTC  |  Data Pulled at: " + CBOLD + str(current_time) + CLEAR + " UTC")
    print("Numbers Drawn: " + final_numbers)
    print("Multiplier: " + str(bonus) + CLEAR)
    print("Heads/Tails Result: " + str(HTresult) + CLEAR + "  |  " + CRED + "Heads: " + str(Hresult) + CBLUE + "  Tails: " + str(Tresult) + CLEAR)
    print("Time Between Games: " + str(differnce))

    if monitor == True:
        calculateWin(mode, numbers_matched)
        if mode == "Classic" or mode == "Mega Million":
            if last_game == True: print("Result: " + CBOLD + str(numbers_matched) + CLEAR + " Numbers Matched  |  Won: " + str(win_display) + "    " + CYELLOW  + CBOLD + "LAST GAME " + CLEAR)
            else: print("Result: " + CBOLD + str(numbers_matched) + CLEAR + " Numbers Matched  |  Won: " + str(win_display))
        elif mode == "Heads / Tails": print("Result: Picked " + str(HTchoice) + "  |  Won: " + str(win_display))
    print(CBLUE + "---------------------------------------------------------------------" + CLEAR)
    last_start_time = start_time

def getData(): ### Extracts data from API Response
    global game_number, draw_numbers, current_time, start_time, bonus, multiplier, HTresult, Hresult, Tresult
    live_data = 0
    live_data = getAPI(live_data)

    ### Game Number
    game_number = live_data["game_number"]

    ### Numbers Drawn
    draw_numbers = live_data["draw_numbers"]
    draw_numbers.sort(key = lambda x: x, reverse = False)

    ### Start Time
    started_at = live_data["started_at"]
    start_time = datetime.datetime.strptime(started_at.split('.')[0],'%Y-%m-%d %H:%M:%S') # Removes milliseconds

    ### Bonus
    bonus = live_data["bonus"]
    if bonus == "reg":
        multiplier = 1
        bonus = CRED + "reg"

    elif bonus == "x2":
        multiplier = 2
        bonus = CYELLOW + "x2"

    elif bonus == "x3":
        multiplier = 3
        bonus = CGREEN + "x3"

    elif bonus == "x4":
        multiplier = 4
        bonus = CBOLD + CGREEN + "x4"

    elif bonus == "x5":
        multiplier = 5
        bonus = CBOLD + CYELLOW + "x5"
    
    elif bonus == "x10":
        multiplier = 10
        bonus = CBOLD + CBLUE + "x10"    
    else: print(CRED + "Error unknown bonus:" + str(bonus))

    ### Heads/Tails
    HTresult = live_data["result"]
    if HTresult == "tails": HTresult = CBOLD + CBLUE + "Tails" 
    elif HTresult == "heads": HTresult = CBOLD + CRED + "Heads"
    elif HTresult == "evens": HTresult = CBOLD + CBEIGE + "Evens"
    Hresult = live_data["heads"] # Number of head numbers
    Tresult = live_data["tails"] # Number of tail numbers

    ### Time
    current_time = datetime.datetime.utcnow()
    current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

def wait():
    if countdown == "True":
        for i in reversed(range(cooldown + 1)): 
            if i == 0: # if countdown is 0 -> clear line
                sys.stdout.write("\r" + CBEIGE + "Next Request in: " + str(i) + " seconds      " + CLEAR)
                sys.stdout.flush()    
                time.sleep(1)
                sys.stdout.write("\r")
                sys.stdout.flush()
            else:    
                sys.stdout.write("\r" + CBEIGE + "Next Request in: " + str(i) + " seconds      " + CLEAR)
                sys.stdout.flush()
                time.sleep(1)
    elif countdown == "Manual":
        input("")
    else:
        time.sleep(cooldown)

def calculateWin(mode, numbers_matched): # There is probably a better way to do this
    global total_numbers, multiplier, multi_status, win_display
    win = "n/a"
    if mode == "Classic" or mode == "Mega Million":
        while win == "n/a":
            if mode == "Classic":
                if total_numbers == 1: win = c_spot1_WinList[numbers_matched]
                elif total_numbers == 2: win = c_spot2_WinList[numbers_matched]
                elif total_numbers == 3: win = c_spot3_WinList[numbers_matched]
                elif total_numbers == 4: win = c_spot4_WinList[numbers_matched]
                elif total_numbers == 5: win = c_spot5_WinList[numbers_matched]
                elif total_numbers == 6: win = c_spot6_WinList[numbers_matched]
                elif total_numbers == 7: win = c_spot7_WinList[numbers_matched]
                elif total_numbers == 8: win = c_spot8_WinList[numbers_matched]
                elif total_numbers == 9: win = c_spot9_WinList[numbers_matched]
                elif total_numbers == 10: win = c_spot10_WinList[numbers_matched]
                elif total_numbers == 15: win = c_spot15_WinList[numbers_matched]
                elif total_numbers == 20: win = c_spot20_WinList[numbers_matched]
                elif total_numbers == 40: win = c_spot40_WinList[numbers_matched]

            elif mode == "Mega Million":
                if total_numbers == 1: win = mm_spot1_WinList[numbers_matched]
                elif total_numbers == 2: win = mm_spot2_WinList[numbers_matched]
                elif total_numbers == 3: win = mm_spot3_WinList[numbers_matched]
                elif total_numbers == 4: win = mm_spot4_WinList[numbers_matched]
                elif total_numbers == 5: win = mm_spot5_WinList[numbers_matched]
                elif total_numbers == 6: win = mm_spot6_WinList[numbers_matched]
                elif total_numbers == 7: win = mm_spot7_WinList[numbers_matched]
                elif total_numbers == 8: win = mm_spot8_WinList[numbers_matched]
                elif total_numbers == 9: win = mm_spot9_WinList[numbers_matched]
                elif total_numbers == 10: win = mm_spot10_WinList[numbers_matched]
                elif total_numbers == 15: win = mm_spot15_WinList[numbers_matched]
                elif total_numbers == 20: win = mm_spot20_WinList[numbers_matched]
                elif total_numbers == 40: win = mm_spot40_WinList[numbers_matched]
        if multi_status == True: win = win*multiplier # calculate bonus (if enabled)
        else: win = win

        if win > 0: win_display = (CGREEN + "$" + str(win) + CLEAR) # green if win
        else: win_display = (CRED + "$" + str(win) + CLEAR) # red if no win

    elif mode == "Heads / Tails":
        if HTresult == HTchoice:
            if HTresult == "Heads" or HTresult == "Tails": 
                win = bet_amount*2
                win_display = (CGREEN + "$" + str(win) + CLEAR) 
            elif HTresult == "Evens": 
                win = bet_amount*4
                win_display = (CGREEN + "$" + str(win) + CLEAR)
        else: 
            win = 0
            win_display = (CRED + "$" + str(win) + CLEAR)   

def endScreen():
    global mode, total_numbers, win_display, multi_status
    print(CBOLD + CBLUE + "Keno Tracker" + CLEAR)
    print(CBOLD + "Keno " + mode + " Ticket Result" + CLEAR + "\n")
    if mode == "Classic" or mode == "Mega Million":
        if multi_status == True: print("Playing Spot " + str(total_numbers) + ", with Bonus Enabled")
        else: print("Playing Spot " + str(total_numbers))
        print("Picked Numbers: " + str(numbers_picked))
        print("Winnings: " + str(win_display))
        print("Games: " + CBOLD + str(start_game) + CLEAR + " - " + CBOLD + str(last_game) + CLEAR) 
        print(CBLUE + "---------------------------------------------------------------------" + CLEAR)
    elif mode == "Heads / Tails":
        pass
    pass

def debug():
    global MainVersion, ConfigVersion, ApiVersion, WinListVersion
    print("/// Debug Menu ///")
    print("Main - " + MainVersion + "\nConfig - " + ConfigVersion + "\nApi - " + ApiVersion + "\nWinList - " + WinListVersion)

while menu_choice == 0: # Main Menu
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("1. Live Game Viewer")
    print("2. Bet Simulator [0%]")
    print("3. Monitor your bet ")
    menu_choice = input("------------->>> ")
    if menu_choice.isnumeric():
        menu_choice = int(menu_choice)
        if menu_choice in m_vaild:
            if menu_choice == 1:
                print("Opening" + CBOLD + " Live Game Viewer" + CLEAR)
                time.sleep(1)
                monitor = False
                print("\n"*4)
            elif menu_choice == 2:
                print("Opening" + CBOLD + " Bet Simulator" + CLEAR)
                time.sleep(1)
                monitor = True
                print("\n"*4)                
            elif menu_choice == 3:
                print("Opening" + CBOLD + " Bet Monitor" + CLEAR)
                time.sleep(1)
                monitor = True
                print("\n"*4)
        else: 
            menu_choice = 0
            print(CRED + "Invaild Option" + CLEAR)
    elif menu_choice == "debug":
        debug()
    else: 
        menu_choice = 0
        print(CRED + "Invaild Option" + CLEAR)

while menu_choice == 1: # Live Game
    getData()
    PrintMainUI()
    wait()

while menu_choice == 2: # Bet Simulator 
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print(CBOLD + "" + CLEAR)

while menu_choice == 3: # Bet Monitor
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print(CBOLD + "Bet Monitor" + CLEAR)
    while monitor_menu_choice == 0:
        print("1. Classic")
        print("2. Mega Millions")
        print("3. Heads / Tails")
        monitor_menu_choice = input("------------->>> ")
        if monitor_menu_choice.isnumeric():
            monitor_menu_choice = int(monitor_menu_choice)
            if monitor_menu_choice in mm_vaild:
                if monitor_menu_choice == 1:
                    print("Opening" + CBOLD + " Classic Keno Monitor" + CLEAR)
                    mode = "Classic"
                    time.sleep(1)
                    print("\n")
                elif monitor_menu_choice == 2:
                    print("Opening" + CBOLD + " Mega Million Keno Monitor" + CLEAR)
                    mode = "Mega Million"
                    time.sleep(1)
                    print("\n")                
                elif monitor_menu_choice == 3:
                    print("Opening" + CBOLD + " Heads / Tails Monitor" + CLEAR)
                    mode = "Heads / Tails"
                    time.sleep(1)
                    print("\n")
            else: 
                monitor_menu_choice = 0
                print(CRED + "Invaild Option" + CLEAR)
        else: 
            monitor_menu_choice = 0
            print(CRED + "Invaild Option" + CLEAR)

    while mode == "Heads / Tails": # Heads / Tails Bet Monitor
        print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
        print(CBOLD + mode + " Keno Monitor" + CLEAR)
        HTchoice = 0  
        while HTchoice == 0:
            HTchoice = input("What outcome have you picked? (heads/tails/evens): ")
            if HTchoice == "tails" or HTchoice == "heads" or HTchoice == "evens":
                HTchoice = HTchoice.capitalize() 
                print("You have chosen " + CBOLD + HTchoice + CLEAR) 
            else: 
                HTchoice = 0
                print(CRED + "Invaild Option" + CLEAR)
        
        check = True
        while check == True:
            getData()
            PrintMainUI()
            wait()

    while mode == "Classic" or mode == "Mega Million": # Keno Bet Monitor
        print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
        print(CBOLD + mode + " Keno Monitor" + CLEAR)
        
        while total_numbers == 0: # How many numbers did the user pick          
            total_numbers = input("How many numbers have been picked: ")
            if total_numbers.isnumeric():
                total_numbers = int(total_numbers)
                if total_numbers not in km_vaild:
                    total_numbers = 0
                    print(CRED + "Invaild Option" + CLEAR)                    
            else: 
                total_numbers = 0
                print(CRED + "Invaild Option" + CLEAR)
        print("Playing " + CBOLD + str(total_numbers) + CLEAR + " Numbers")

        print("Input your picks, type in one number per line")
        for i in range(total_numbers): # Enter chosen numbers
            pick = 0
            while pick == 0: 
                pick = input("")
                if pick.isnumeric():
                    pick = int(pick)
                    if pick in numbers_picked:
                        print(CRED + "You have already chosen " + str(pick) + CLEAR)
                        pick = 0
                    elif pick not in range(1,80 + 1):
                        pick = 0
                        print(CRED + "Invaild Option" + CLEAR)
                else:
                    pick = 0
                    print(CRED + "Invaild Option" + CLEAR)
            numbers_picked.append(pick)
            numbers_picked_display.append(pick)
        numbers_picked_display.sort(key = lambda x: x, reverse = False)
        numbers_picked_display = ", ".join(map(str, numbers_picked_display))
        print("Numbers Picked: " + str(numbers_picked_display))

        while final_game == 0:
            final_game = input("What is the final game on the ticket: ")
            if final_game.isnumeric():
                final_game = int(final_game)
                if final_game not in range(0,999 + 1): # must be in 000-999 ### No functionality yet
                    final_game = 0
                    print(CRED + "Invaild Option" + CLEAR)     
            else:
                final_game = 0
                print(CRED + "Invaild Option" + CLEAR) 
        print("Final game is: " + CBOLD + str(final_game) + CLEAR)

        while multi_status == -1:
            multi_status = input("Is Keno Bonus on? (y/n): ")
            if multi_status == "y": multi_status = True
            elif multi_status == "n": multi_status = False  
            else: 
                multi_status = -1
                print(CRED + "Invaild Option" + CLEAR)     

        print(CBLUE + "-----------------------------------" + CLEAR)  
        print(CBOLD + "Ticket information" + CLEAR)
        print(mode + " Keno")
        print("Total Numbers: " + str(total_numbers))
        print("Picked Numbers: " + str(numbers_picked))
        print("Ending Game: " + str(final_game))
        print("Bonus Enabled: " + str(multi_status))
        input("Press [Enter] to start")
        print("")
        getData() ### TEMP solution, find a way to get data on launch 
        # Get timing on how often a game starts then add an auto cooldown setting
        # CHECK WHAT HAPPENS WHEN A GAME IS 00X AND WHEN final_game = X
        start_game = game_number
        last_game = False
        print(game_number) 
        print(final_game)
        while game_number != final_game + 1: # Allows last game to be shown
            if final_game == game_number: # If last game go to 'end screen' after showing data
                last_game = True
                getData()
                PrintMainUI()
                input("Press [Enter] to see ticket results")
                while True: endScreen() # END OF PROGRAM

            else:
                getData()
                PrintMainUI()
                wait()
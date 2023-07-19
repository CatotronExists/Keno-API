from keno import keno_app
from Api import getAPI, ApiVersion
from Config import cooldown, countdown, ConfigVersion
from WinList import *
import time
import datetime
from datetime import timedelta
import sys

### FIND HOW OFTEN A GAME STARTS (seems to be every 2:40 ~160sec)
### GET THE API REQUEST ~5-10 SECONDS AFTER GAME START

### TODO Before v0.2   est. (25/07)
# Add Jackpot Support
# Change config of cooldown -> allow cooldown to be set to "Auto"
#   Add config checks to ensure vaild values
# FIX same game cooldown 
# Fix: The Time between data pulls gets ~1-3 seconds added each time

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

MainVersion = "v0.1.d-27"
menu_choice = -1
total_numbers = 0
numbers_picked = []
m_vaild = [1, 2, 3, "debug"] # Menu vaild choices
mm_vaild = [1, 2, 3] # Monitor Menu vaild choices
km_vaild = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40] # Keno Monitor (vaild number of chosen numbers)
numbers_picked = []
numbers_picked_display = []
total_win = 0
first_cooldown = True
in_menus = True
main = False
bet_amount = 1 # temp solution for h/t

def PrintMainUI(): ### Build Terminal Output
    global HTresult_display
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

    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("Game Number: " + CBOLD + str(game_number) + CLEAR + "  |  Game Started at: " + CBOLD + str(start_time) + CLEAR + " UTC  |  Data Pulled at: " + CBOLD + str(current_time) + CLEAR + " UTC")
    print("Numbers Drawn: " + final_numbers)
    print("Multiplier: " + str(bonus) + CLEAR)
    print("Heads/Tails Result: " + str(HTresult_display) + CLEAR + "  |  " + CRED + "Heads: " + str(Hresult) + CBLUE + "  Tails: " + str(Tresult) + CLEAR)

    if monitor == True:
        calculateWin(mode, numbers_matched)
        if mode == "Classic" or mode == "Mega Million":
            if last_game == True: print("Result: " + CBOLD + str(numbers_matched) + CLEAR + " Numbers Matched  |  Won: " + str(win_display) + "    " + CYELLOW  + CBOLD + "LAST GAME " + CLEAR)
            else: print("Result: " + CBOLD + str(numbers_matched) + CLEAR + " Numbers Matched  |  Won: " + str(win_display))
        else:
            if last_game == True: print("Result: Picked " + str(HTchoice) + "  |  Won: " + str(win_display) + "    " + CYELLOW  + CBOLD + "LAST GAME " + CLEAR)
            else: print("Result: Picked " + str(HTchoice) + "  |  Won: " + str(win_display))
    print(CBLUE + "---------------------------------------------------------------------" + CLEAR)

def getData(): ### Extracts data from API Response
    global game_number, draw_numbers, current_time, start_time, bonus, multiplier, HTresult, Hresult, Tresult, started_at, HTresult_display
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

    ### Current Time
    now_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.datetime.strptime(now_time.split('.')[0],'%Y-%m-%d %H:%M:%S') # Removes milliseconds

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
    HTresult = HTresult.capitalize() 
    if HTresult == "Tails": HTresult_display = CBOLD + CBLUE + "Tails" + CLEAR
    elif HTresult == "Heads": HTresult_display = CBOLD + CRED + "Heads" + CLEAR
    elif HTresult == "Evens": HTresult_display = CBOLD + CBEIGE + "Evens" + CLEAR
    Hresult = live_data["heads"] # Number of head numbers
    Tresult = live_data["tails"] # Number of tail numbers

def wait():
    global cooldown, first_wait, first_cooldown
    if first_cooldown == True:
        saved_cooldown = cooldown
        cooldown = first_wait 
        cooldown = int(cooldown)
        cooldown += 10
        if cooldown < 0: cooldown = 0
    
    if cooldown > 0:
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
        elif countdown == "Manual": input("")
        else: time.sleep(cooldown)

    if first_cooldown == True:
        cooldown = saved_cooldown 
        first_cooldown = False

def calculateWin(mode, numbers_matched):
    global total_numbers, multiplier, multi_status, win_display, total_win
    win = "n/a"
    if mode == "Classic" or mode == "Mega Million":
        if mode == "Classic": win = Classic_Winlists[total_numbers][numbers_matched] * bet_amount
        elif mode == "Mega Million": win = MegaMillion_Winlists[total_numbers][numbers_matched] * bet_amount

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
    total_win += win   

def endScreen():
    print(CBOLD + CBLUE + "Keno Tracker" + CLEAR)
    print(CBOLD + "Keno " + mode + " Ticket Result" + CLEAR)
    if mode == "Classic" or mode == "Mega Million":
        if multi_status == True: print("Playing Spot " + str(total_numbers) + ", with Bonus Enabled")
        else: print("Playing Spot " + str(total_numbers))
        print("Picked Numbers: " + str(numbers_picked))
        print("Winnings: $" + str(total_win))
        print("Games: " + CBOLD + str(start_game) + CLEAR + " - " + CBOLD + str(final_game) + CLEAR + " Total Games: " + str(total_games)) 
    elif mode == "Heads / Tails":
        print("Predicted Outcome: " + str(HTchoice))
        print("Outcome: " + str(HTresult))
        print("Winnings: $" + str(total_win))
        print("Game: " + str(last_game))
    print(CBLUE + "---------------------------------------------------------------------" + CLEAR)

def configCheck():
    global app, cooldown, countdown
    pass
def debug():
    global MainVersion, ConfigVersion, ApiVersion, WinListVersion
    print("/// Debug Menu ///")
    print("Main - " + MainVersion + "\nConfig - " + ConfigVersion + "\nApi - " + ApiVersion + "\nWinList - " + WinListVersion)

configCheck()
while menu_choice == -1: # Main Menu
    getData()
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("1. Live Game Viewer")
    print("2. Bet Simulator [0%]")
    print("3. Monitor your bet ")
    print("Current Game: " + str(game_number))
    menu_choice = input("------------->>> ")
    if menu_choice.isnumeric():
        menu_choice = int(menu_choice)
        if menu_choice in m_vaild:
            if menu_choice == 1: print("Opening" + CBOLD + " Live Game Viewer" + CLEAR)
            elif menu_choice == 2: print("Opening" + CBOLD + " Bet Simulator" + CLEAR)                
            elif menu_choice == 3: print("Opening" + CBOLD + " Bet Monitor" + CLEAR)
        else: 
            menu_choice = -1
            print(CRED + "Invaild Option" + CLEAR)
    elif menu_choice == "debug": debug()
    else: 
        menu_choice = -1
        print(CRED + "Invaild Option" + CLEAR)

while menu_choice != 0:
    monitor = False
    time.sleep(1)
    print("\n"*4)
    if menu_choice == 1: in_menus == False # Live Game Viewer
    elif in_menus == True: 
        monitor = True
        while menu_choice == 2: # Bet Simulator 
            print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
            print(CBOLD + "" + CLEAR) 
            print(CRED + CBOLD + "Bet Simulator is not complete at this time" + CLEAR)
            time.sleep(0.5)
            print(CRED + CBOLD + "Rerouting to Live Game Viewer..." + CLEAR)
            time.sleep(1)
            menu_choice = 0 
            in_menus = monitor = main = False    

        while menu_choice == 3: # Bet Monitor
            print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
            print(CBOLD + "Bet Monitor" + CLEAR)
            monitor_menu_choice = 0
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

            if mode == "Heads / Tails": # Heads / Tails Bet Monitor
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

                bet_amount = 0
                while bet_amount == 0:
                    bet_amount = input("What is the bet amount\n$")
                    if bet_amount.isnumeric(): bet_amount = int(bet_amount)
                    else: 
                        bet_amount = 0
                        print(CRED + "Invaild Option" + CLEAR) 
                
                final_game = -1
                while final_game == -1:
                    final_game = input("What game is this bet for: ")
                    if final_game.isnumeric():
                        final_game = int(final_game)
                        if final_game not in range(0,999 + 1): # must be in 000-999 ### No functionality yet
                            final_game = -1
                            print(CRED + "Invaild Option" + CLEAR)  
                    else:
                        final_game = -1
                        print(CRED + "Invaild Option" + CLEAR) 

                menu_choice = 0 
                in_menus = False

            elif mode == "Classic" or mode == "Mega Million": # Keno Bet Monitor
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
                                pick = 0
                                print(CRED + "You have already chosen " + str(pick) + CLEAR)
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

                start_game = -1
                while start_game == -1: 
                    start_game = input("What is the first game on the ticket: ")
                    if start_game.isnumeric():
                        start_game = int(start_game)
                        if start_game not in range(0,999 + 1): # must be in 000-999 ### No functionality yet
                            start_game = -1
                            print(CRED + "Invaild Option" + CLEAR)     
                    else:
                        start_game = -1
                        print(CRED + "Invaild Option" + CLEAR) 
                print("Starting game is: " + CBOLD + str(start_game) + CLEAR)

                final_game = -1
                while final_game == -1:
                    final_game = input("What is the final game on the ticket: ")
                    if final_game.isnumeric():
                        final_game = int(final_game)
                        if final_game not in range(0,999 + 1): # must be in 000-999 ### No functionality yet
                            final_game = -1
                            print(CRED + "Invaild Option" + CLEAR)  
                        elif final_game == start_game:
                            final_game = -1
                            print(CRED + "Invaild Option" + CLEAR)  
                    else:
                        final_game = -1
                        print(CRED + "Invaild Option" + CLEAR) 
                print("Final game is: " + CBOLD + str(final_game) + CLEAR)
                total_games = start_game - final_game
                if total_games < 0: # if games selected 'wrap around' e.g 989 to 4
                    total_games = final_game - start_game

                if mode == "Classic":
                    multi_status = -1
                    while multi_status == -1:
                        multi_status = input("Is Keno Bonus on? (y/n): ")
                        if multi_status == "y": multi_status = True
                        elif multi_status == "n": multi_status = False  
                        else: 
                            multi_status = -1
                            print(CRED + "Invaild Option" + CLEAR)
                else: multi_status = False

                bet_amount = 0                       
                while bet_amount == 0:
                    bet_amount = input("What is the bet amount\nIf you have bonus on, half the bet amount shown on your ticket\n$")
                    if bet_amount.isnumeric(): 
                        bet_amount = int(bet_amount)
                        if bet_amount == 0 or bet_amount < 0: 
                            bet_amount = 0
                            print(CRED + "Invaild Option" + CLEAR)     
                    else: 
                        bet_amount = 0
                        print(CRED + "Invaild Option" + CLEAR)      

                print(CBLUE + "-----------------------------------" + CLEAR)  
                print(CBOLD + "Ticket information" + CLEAR)
                print(mode + " Keno")
                print("Total Numbers: " + str(total_numbers))
                print("Picked Numbers: " + str(numbers_picked))
                print("Ending Game: " + str(final_game))
                if mode == "Classic": print("Bonus Enabled: " + str(multi_status))
                print("Bet per game: " + str(int(bet_amount/total_games)))
                input("Press [Enter] to start\n")
                if (start_time - current_time) < timedelta(minutes=2, seconds=45): first_cooldown = True
                last_game = False
                menu_choice = 0 
                in_menus = False
                    
    while in_menus == False:
        while first_cooldown == True:
            time_delta = current_time - start_time
            first_wait = time_delta.total_seconds()
            first_wait = cooldown - first_wait
            if final_game == game_number: # If last game go to 'end screen' after showing data
                last_game = True
                getData()
                PrintMainUI()
                input("Ticket Complete! Press [Enter] to see ticket results ")
                print("")
                endScreen()
                time.sleep(999) 
            else:
                PrintMainUI()
                wait()
                main == True
            
        if final_game - 1 == game_number: # If last game go to 'end screen' after showing data
            last_game = True
            getData()
            PrintMainUI()
            input("Ticket Complete! Press [Enter] to see ticket results ")
            print("")
            endScreen()
            time.sleep(999)  

        elif main == True:
            getData()
            PrintMainUI()
            wait()
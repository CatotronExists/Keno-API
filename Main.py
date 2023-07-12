from keno import keno_app
from Api import getAPI
from Config import cooldown, countdown
import time
import datetime
import sys

### FIND HOW OFTEN A GAME STARTS
### GET THE API REQUEST ~10 SECONDS AFTER GAME START

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

menu_choice = 0
monitor_menu_choice = 0
total_numbers = 0
numbers_picked = []
m_vaild = [1, 2, 3] # Menu vaild choices
mm_vaild = [1, 2, 3] # Monitor Menu vaild choices
ckm_vaild = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40] # Classic Keno Monitor (vaild number of chosen numbers)

def PrintMainUI(): ### Build Terminal Output
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
    print("Heads/Tails Result: " + str(HTresult) + CLEAR + "  |  " + CRED + "Heads: " + str(Hresult) + CBLUE + "  Tails: " + str(Tresult) + CLEAR)
    if monitor == True:
        print("Result: " + CBOLD + str(numbers_matched) + CLEAR + " Numbers Matched  |  Won: " + str(multiplier))
    print(CBLUE + "---------------------------------------------------------------------")

def SortData(): ### Extracts data from API Response
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

while menu_choice == 0: # Main Menu
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print("1. Live Game Viewer")
    print("2. Bet Simulator [Soon]")
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
    else: 
        menu_choice = 0
        print(CRED + "Invaild Option" + CLEAR)

while menu_choice == 1: # Live Game
    SortData()
    PrintMainUI()
    if countdown == "True":
        for i in reversed(range(cooldown + 1)): 
            if i == 0:
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

while menu_choice == 2: # Bet Simulator 
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print(CBOLD + "" + CLEAR)

while menu_choice == 3: # Bet Monitor
    print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
    print(CBOLD + "Bet Monitor" + CLEAR)
    while monitor_menu_choice == 0:
        print("1. Classic")
        print("2. Mega Millions [Soon]")
        print("3. Heads / Tails [Soon]")
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
    while monitor_menu_choice == 1: # Classic Keno Bet Monitor
        print(CBOLD + CBLUE + "Keno Tracker                  " + CLEAR)
        print(CBOLD + "Classic Keno Monitor" + CLEAR)
        while total_numbers == 0: # How many numbers were chosen          
            total_numbers = input("How many numbers have been picked: ")
            if total_numbers.isnumeric():
                total_numbers = int(total_numbers)
                if total_numbers not in ckm_vaild:
                    total_numbers = 0
                    print(CRED + "Invaild Option" + CLEAR)                    
            else: 
                total_numbers = 0
                print(CRED + "Invaild Option" + CLEAR)
        print("Playing " + CBOLD + str(total_numbers) + CLEAR + " Numbers")
        print("Input your picks, type in one number per line")
        numbers_picked = []
        numbers_picked_display = []
        for i in range(total_numbers): # Pick chosen numbers
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
        final_game = 0
        while final_game == 0:
            final_game = input("What is the final game on the ticket: ")
            if final_game.isnumeric():
                final_game = int(final_game)
                if final_game not in range(0,999 + 1): # must be in 000-999
                    final_game = 0
                    print(CRED + "Invaild Option" + CLEAR)     
            else:
                final_game = 0
                print(CRED + "Invaild Option" + CLEAR) 
        multi_status = -1
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
        input("Press [Enter] to start ")
        print("")
        check = True
        while check == True:
            SortData()
            ### Win Calcuation
            #win = numbers_matched
            PrintMainUI()
            if countdown == True:
                for i in reversed(range(cooldown + 1)): 
                    if i == 0:
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
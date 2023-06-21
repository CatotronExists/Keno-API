import requests
import keno
from keno import keno_app
import time
import datetime
import os
os.system("")
CLEAR = '\33[0m'
CGREEN = '\33[92m'
CGREENHIGHLIGHT = '\33[102m'
CBLUE = '\33[34m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CBEIGE = '\33[36m'


app = keno_app.KenoAPI("VIC") # choose the state you would like you to get data from
mode = 1

if mode == 1:
    while mode == 1: # Live Game
        try: 
            live_data = app.live_draw()
        except Exception as e:
            print(CRED + str(e))

        ### Numbers Drawn
        numbers = live_data["draw_numbers"]
        numbers.sort(key = lambda x: x, reverse = False)
        draw_numbers = ", ".join(map(str, numbers))
        ### Game Number
        game_number = live_data["game_number"]
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
            bonus = CGREENHIGHLIGHT + "x4"
        
        else: print(CRED + "Error unknown bonus:" + str(bonus)) # incase there is any higher multiplier

        ### Heads/Tails
        HTresult = live_data["result"]
        if HTresult == "tails": HTresult = CBLUE + "Tails"
        elif HTresult == "heads": HTresult = CRED + "Heads"
        elif HTresult == "evens": HTresult = CBEIGE + "Evens"
        Hresult = live_data["heads"]
        Tresult = live_data["tails"]

        ### Time
        current_time = datetime.datetime.utcnow()
        current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        ### Build Terminal
        print(CBLUE + "Keno Tracker" + CLEAR)
        print("Game Number: " + str(game_number) + "  |  Game Started at: " + str(start_time) + " UTC  |  Data Pulled at: " + str(current_time) + " UTC")
        print("Numbers Drawn: " + CGREEN + draw_numbers + CLEAR)
        print("Multiplier: " + str(bonus) + CLEAR)
        print("Heads/Tails Result: " + str(HTresult) + CLEAR + "  |  " + CRED + "Heads: " + str(Hresult) + CBLUE + "  Tails: " + str(Tresult) + CLEAR)
        print(CBLUE + "---------------------------------------------------------------------")

        time.sleep(180) # Adjust to be closer to start time

elif mode == 2: # Hot/Cold
    trending_numbers = app.hot_cold()
    print(trending_numbers)

    print("-------------------------\\\\\\")
    cold = trending_numbers['cold']
    cold_numbers = ', '.join(map(str, cold))
    print("Cold Numbers: " + cold_numbers)

    hot = trending_numbers['hot']
    hot_numbers = ', '.join(map(str, hot))
    print("Hot Numbers: "+ hot_numbers)

    last_update = trending_numbers['last_updated']
    print("Last Updated: "+str(last_update)+" seconds ago")
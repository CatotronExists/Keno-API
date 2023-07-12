from keno import keno_app
from Config import app
import time

ApiVersion = "v0.1.d-18"
CRED = '\33[91m'
CLEAR = '\33[0m'

last_game_number = "n/a"
def getAPI(live_data):
    while live_data == 0:
        try: 
            live_data = app.live_draw()
            game_number = live_data["game_number"]
            if last_game_number == game_number: # in case the same game is called twice, try again after 20 sec ### To Fix
                print(CRED + "Already Fetched Game: " + str(game_number) + "     " + CLEAR)
                live_data = 0
                time.sleep(20)
            last_game_number == game_number
            return live_data
        except Exception as e:
            print(CRED + str(e) + CLEAR)
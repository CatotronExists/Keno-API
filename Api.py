from keno import keno_app
from Config import app
from WinList import UpdateJackpots
import time

apiVersion = "v0.3.d-3"

CRED = '\33[91m'
CLEAR = '\33[0m'

def GetJackpots():
    global c_spot7_jackpot, c_spot8_jackpot, c_spot9_jackpot, c_spot10_jackpot, mm_spot7_jackpot, mm_spot8_jackpot, mm_spot9_jackpot, mm_spot10_jackpot
    raw_jackpots = app.jackpot()
    c_spot7_jackpot = raw_jackpots["regular"]["seven_spot"]
    c_spot8_jackpot = raw_jackpots["regular"]["eight_spot"]
    c_spot9_jackpot = raw_jackpots["regular"]["nine_spot"]
    c_spot10_jackpot = raw_jackpots["regular"]["ten_spot"]
    mm_spot7_jackpot = raw_jackpots["leveraged"]["seven_spot"]
    mm_spot8_jackpot = raw_jackpots["leveraged"]["eight_spot"]
    mm_spot9_jackpot = raw_jackpots["leveraged"]["nine_spot"]
    mm_spot10_jackpot = raw_jackpots["leveraged"]["ten_spot"]
    UpdateJackpots()
    
last_game_number = "n/a"
def GetAPI(liveData):
    while liveData == 0:
        try: 
            time.sleep(0.1)
            liveData = app.live_draw()
            game_number = liveData["game_number"]
            if last_game_number == game_number: # in case the same game is called twice, try again after 10 sec
                print(CRED + "Already Fetched Game: " + str(game_number) + " Retrying in 10 seconds..." + CLEAR)
                liveData = 0
                time.sleep(10)
            last_game_number == game_number
            return liveData
        except Exception as e: print(CRED + str(e) + CLEAR)
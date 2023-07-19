from keno import keno_app
from Config import app
import time

ApiVersion = "v0.1.d-28"
CRED = '\33[91m'
CLEAR = '\33[0m'

def getJackpots():
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
    print(c_spot10_jackpot)

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
        except Exception as e: print(CRED + str(e) + CLEAR)
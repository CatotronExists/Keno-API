### KENO DATAVIS ###
## WINLIST.PY ##
# Win Lists #
# Index 0 = 0 numbers matched, Index 1 = 1 number matched, etc.
# If a value = 0 then there is no prize for that number of matches. eg. Index 3 = 0, 3 numbers matched but a reward of 0
winListVersion = "Legacy-08/2023-1"
c_spot7_jackpot = c_spot8_jackpot = c_spot9_jackpot = c_spot10_jackpot = mm_spot7_jackpot = mm_spot8_jackpot = mm_spot9_jackpot = mm_spot10_jackpot = 0
def UpdateJackpots():
    global c_spot7_jackpot, c_spot8_jackpot, c_spot9_jackpot, c_spot10_jackpot, mm_spot7_jackpot, mm_spot8_jackpot, mm_spot9_jackpot, mm_spot10_jackpot 
    from Api import c_spot7_jackpot, c_spot8_jackpot, c_spot9_jackpot, c_spot10_jackpot, mm_spot7_jackpot, mm_spot8_jackpot, mm_spot9_jackpot, mm_spot10_jackpot
### Classic Keno Win Lists
ClassicWinlists = [
    [0], # makes Index easier to work with
    [0, 3], #c_spot1_WinList
    [0, 0, 12], #c_spot2_WinList
    [0, 0, 1, 44], #c_spot3_WinList
    [0, 0, 1, 3, 120], #c_spot4_WinList
    [0, 0, 0, 2, 14, 640], #c_spot5_WinList
    [0, 0, 0, 1, 5, 80, 1800], #c_spot6_WinList
    [0, 0, 0, 1, 3, 12, 125, c_spot7_jackpot], #c_spot7_WinList
    [0, 0, 0, 0, 2, 7, 60, 675, c_spot8_jackpot], #c_spot8_WinList
    [0, 0, 0, 0, 1, 5, 20, 210, 2500, c_spot9_jackpot], #c_spot9_WinList
    [0, 0, 0, 0, 1, 2, 6, 50, 580, 10000, c_spot10_jackpot], #c_spot10_WinList
    [0],
    [0],
    [0],
    [0],
    [0, 0, 0, 0, 0, 1, 2, 4, 20, 50, 250, 2000, 12000, 50000, 100000, 250000], #c_spot15_WinList
    [0],
    [0],
    [0],
    [0],
    [100, 10, 2, 0, 0, 0, 0, 0, 2, 7, 20, 100, 450, 1200, 5000, 10000, 15000, 25000, 50000, 100000, 250000], #c_spot20_WinList
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [250000, 25000, 2200, 35, 7, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 7, 35, 200, 2200, 25000, 250000] #c_spot40_WinList
]

### Mega Million Win Lists
MegaMillionWinlists = [
    [0], # makes Index easier to work with
    [0, 6], #mm_spot1_WinList
    [0, 0, 25], #mm_spot2_WinList
    [0, 0, 2, 90], #mm_spot3_WinList
    [0, 0, 2, 7, 260], #mm_spot4_WinList
    [0, 0, 1, 3, 14, 1300], #mm_spot5_WinList
    [0, 0, 0, 2, 10, 160, 3800], #mm_spot6_WinList
    [0, 0, 0, 2, 6, 20, 280, mm_spot7_jackpot], #mm_spot7_WinList
    [0, 0, 0, 1, 2, 10, 100, 1280, mm_spot8_jackpot], #mm_spot8_WinList
    [0, 0, 0, 1, 2, 6, 20, 300, 5200, mm_spot9_jackpot], #mm_spot9_WinList
    [0, 0, 0, 0, 2, 4, 7, 50, 600, 11000, mm_spot10_jackpot], #mm_spot10_WinList
    [0],
    [0],
    [0],
    [0],
    [0, 0, 0, 0, 0, 2, 4, 6, 45, 120, 500, 5000, 15000, 75000, 200000, 500000], #mm_spot15_WinList
    [0],
    [0],
    [0],
    [0],
    [150, 12, 5, 1, 0, 0, 0, 1, 5, 12, 25, 150, 650, 1500, 7500, 20000, 50000, 75000, 100000, 200000, 500000], #mm_spot20_WinList
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [500000, 50000, 2700, 250, 50, 10, 6, 2, 1, 0, 0, 0, 1, 2, 6, 10, 50, 250, 3700, 50000, 500000] #mm_spot40_WinList
]
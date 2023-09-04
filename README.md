# Keno-DataVis
A program that gets data from Keno using an API for the purpose of displaying and interacting with the data. For now the program is in it's early stages, only a basic command line interface for now but there is alot planned. 

## Branches
[Legacy](https://github.com/CatotronExists/Keno-DataVis/tree/Legacy) - A version where the program is Command Line Based (without Databasing)\
[ActiveDev](https://github.com/CatotronExists/Keno-DataVis/tree/ActiveDev) - Place to test developement as it happens

### Setup 
**NOTE: WHEN SWITCHING BETWEEN VERSIONS IT IS BEST TO DROP/DELETE THE MONGODB DATABASE**

0. Download all files for your version of choice, I Recommend either Latest Release or Last ActiveDev Branch Commit
1. Go to the [Keno-API pypi page](https://pypi.org/project/kenoAPI/) and follow instructions to download the package.
2. You also need the following packages, [Certifi](https://pypi.org/project/certifi/) and [Pymongo](https://pypi.org/project/pymongo/)
3. Then Follow the Guide for your version (https://github.com/CatotronExists/Keno-DataVis/wiki)
4. Run Setup.py, if any errors occur repeat step 3 then open an issue with the 'help' label.

### Credits
API Created by "JGolafshan" - Joshua Golafshan [API](https://github.com/JGolafshan/keno-api)

Win Data sourced from [Keno Game Guide](https://www.keno.com.au/keno-pdfs/VIC_Game%20Guide.pdf)\
*Data is sourced from the Victorian version, win amounts are the same across all states (as of now). If any win data is wrong, open an issue!*

### Check List
#### Legacy
- [x] Gets data and Displays in easy to read format
- [x] Simulate betting (using a virtual money system, choose numbers and see how much you would win)
  - [x] Compatible with Custom Numbers and "Kwikpik"
- [x] Ability to input your bet and display results in real time
  - [x] Displays total winnings (per game and total)
  - [x] Compatible with different modes (Mega Millions, Classic, T/H)
#### Main
- [x] Saves Data to a database
- [ ] Web page to display data from database
- [ ] Full Breakdown of data
- [ ] Predict most likely to win numbers using trends?

### Roadmap to v1.0
- [ ] v1.0 | Completion (xx/xx/2023)
- [ ] v0.9 | Browsing Data (xx/xx/2023)
- [ ] v0.8 | Trends and Graphs (xx/xx/2023)
- [ ] v0.7 | Data Visualised (xx/xx/2023)
- [ ] v0.6 | User Input Returns (xx/xx/2023)
- [x] v0.5 | HTML Interface (4/09/2023)
- [x] v0.4 | Database Connection (15/08/2023)
- [x] v0.3 | Bet Simulation (25/07/2023)
- [x] v0.2 | Bet Monitoring (22/07/2023)
- [x] v0.1 | First Stable Release (21/06/2023)

### Disclaimer
This program is being made for educational purposes only, use at your own risk.
If you wish to use this program you have to download and run it on your machine, there will be no public database. You have to collect it, which can be done with this program.

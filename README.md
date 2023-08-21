# Keno-DataVis
A program that gets data from Keno using an API for the purpose of displaying and interacting with the data. For now the program is in it's early stages, only a basic command line interface for now but there is alot planned. 

## ActiveDev Branch
As work is complete it will be put here, each commit has a version with it.
When creating an issue on the ActiveDev Branch be sure to include the full version.

### Versions
**Python**
If you encounter any issues type 'debug' into the main menu.
It will output the file versions, cross check those versions below

Main - v0.4\
Config - v0.3.d-1\
Api - v0.3.d-3\
WinList - v0.3.d-1\
Setup - v0.3.d-6

**HTML**
Scroll to the footer and look for *// Version v---*\
Index - v0.4.d-2

If the versions don't match, download the latest version (This can be found by navigating to the commit list and looking for the last commit with a version in the name). If the issue persists open an issue [here](https://github.com/CatotronExists/Keno-DataVis/issues)

### Setup 
**NOTE: WHEN SWITCHING BETWEEN DEV VERSIONS IT IS BEST TO DROP/DELETE THE MONGODB DATABASE**

0. Download all files in the ActiveDev Branch/Latest Release
1. Go to the [Keno-API pypi page](https://pypi.org/project/kenoAPI/) and follow instructions to download the package.
2. You also need the following packages, [Certifi](https://pypi.org/project/certifi/) and [Pymongo](https://pypi.org/project/pymongo/)
3. Follow this [Database Setup Guide](https://gist.github.com/CatotronExists/2776b4175cb21c23d10f16a62a3f68f0)
4. Run Setup.py, if any errors occur repeat step 3 then open an issue with the 'help' label.

### Credits
API Created by "JGolafshan" - Joshua Golafshan [API](https://github.com/JGolafshan/keno-api)

Win Data sourced from [Keno Game Guide](https://www.keno.com.au/keno-pdfs/VIC_Game%20Guide.pdf)\
*Data is sourced from the Victorian version, win amounts are the same across all states (as of now). If any win data is wrong, open an issue!*

### Roadmap to v0.5
- [ ] v0.5 | Migration to Python Backend, Html Frontend    EST.(2x/08/2023)
  - [ ] Basic HTML is Complete [v0.4.d-??]
  - [ ] Further work to UI [v0.4.d-??]
  - [ ] Start Migration away from a Command Line Input [v0.4.d-??]\
    *This will remove most user input, As the plan is to only have the python script getting the API data*
  - [ ] Fetch and Display Data [v0.4.d-??]
  - [x] Create Basic HTML Interface [v0.4.d-1]
- [x] v0.4 | Database Connection (15/08/2023)\
*More may be added/removed as development progresses*

### Disclaimer
This program is being made for educational purposes only, use at your own risk.
If you wish to use this program you have to download and run it on your machine, there will be no public database. You have to collect it, which can be done with this program.
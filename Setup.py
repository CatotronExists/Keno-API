### DATABASE SETUP FOR KENO DATAVIS ###
import time
import json
import pymongo
import certifi
ca = certifi.where()

# Terminal Colors #
import os
os.system("")
CLEAR = '\33[0m'
CGREEN = '\33[92m'
CBLUE = '\33[34m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CBEIGE = '\33[36m'
CBOLD = '\033[1m'
#                #

    # Vars #
if __name__ == "__main__": # Python should ingore prints/input on import :/
    error = False
    credentials = 0
    path = './Credentials.json'
    file = os.path.exists(path)
    #      #

    if file == True:
        with open('Credentials.json') as jsonFile:
            data = json.load(jsonFile)
            setup = data["setup"]
    else: setup = False

    if setup == "True": input(CRED + "Setup has been completed before, delete Credentials.json and relaunch to setup again" + CLEAR)
    elif setup == False: # start
        input(CRED + "Setup Process hasn't been fully tested, it may not fully work at this time. Press [Enter] to Proceed anyway" + CLEAR)
        print(CYELLOW + "Preforming First Time Setup..." + CLEAR)
        time.sleep(1)
        print(CYELLOW + "Complete the intructions in this guide before proceeding\n    " + CLEAR + CBLUE + "[Link to github gist page (soon)] " + CLEAR)
        time.sleep(0.3)
        input("If you have already completed those intructions, Press [Enter] to proceed")

        # Credential Inputs

        print(CYELLOW + "Proceeding with Setup..." + CLEAR)
        while credentials == 0:
            user = input("Enter your username\n" + CYELLOW + "--->> " + CLEAR)
            password = input("Enter your password\n" + CYELLOW + "--->> " + CLEAR)
            restOfString = input("Enter the contents of the connection string after the \"@\"\n" + CYELLOW + "--->> " + CLEAR)

            credentials = "mongodb+srv://" + str(user) + ":" + str(password) + str(restOfString)

            input(CBOLD + CYELLOW + "\n[Full Credentials, Do not share this with anyone] | Press [Enter] to proceed to next step\n" + CLEAR + CBLUE + str(credentials) + CLEAR)
            print(CYELLOW + "Pinging Database..." + CLEAR)
            client = pymongo.MongoClient(credentials, tlsCAFile=ca)
            try: # Send to MongoDB
                client.admin.command('ping')
                print(CGREEN + "         Successfully connected to MongoDB" + CLEAR)
            except Exception as e: 
                error = True
                credentials = 0
                print(CYELLOW + "An Error has occured\n" + CLEAR + CRED + str(e) + CLEAR + "\nCheck if you entered your credentials correctly!")

        if error != True:
            print(CYELLOW + "Configuring Database...")
            try: 
                db = client["kenoGameData"] # defines db (database)
                gameDataDB = db["GameData"] # defines GameData (GameData Storage)
            except Exception as e: 
                error = True
                print(CYELLOW + "An Error has occured\n" + CLEAR + CRED + str(e) + CLEAR + "\nCheck if you setup MongoDB correctly!")

        if error != True:
            print(CYELLOW + "         Vaildating Changes..." + CLEAR)
            time.sleep(0.7)
            try:
                db.validate_collection("GameData")
            except Exception as e: 
                error = True
                input(CYELLOW + "An Error has occured\n" + CLEAR + CRED + str(e) + CLEAR + "\nCheck if you set MongoDB permissions correctly!")

        if error != True:
            print(CGREEN + "                  Database Configured Successfully" + CLEAR)
            time.sleep(0.7)
            print(CYELLOW + "Saving Credentials to Credentials.json..." + CLEAR)
            setup = "True"
            saveData = {'user': user, 'password': password, 'restOfString': restOfString, 'setup': setup}
            with open('Credentials.json', 'w') as outfile:
                json.dump(saveData, outfile, indent=4)

            input(CGREEN + "Setup is complete, you may now close this window\n" + CLEAR) ### END

setupVersion = "v0.3.d-3"

### PREFORM FULL TEST RUN + document steps

###
# Create a mongodb account [here](link)
# 

# make sure your user is an atlas admin
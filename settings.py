import os
import json

def loadSettings():
    if os.path.isfile("settings.cfg"):
        with open('settings.cfg', 'r') as f:
            config = json.load(f)

        return config

    else:
        #create default settings file
        config = {"updatetime" : "10" ,"font": "./fonts/OpenSans-Semibold.ttf","fontsize": '10', "url": "https://pastebin.com/raw/1sehACD5" , "model" : "3" , "slidetime" : "1.5" }

        with open('settings.cfg', 'w') as f:
            json.dump(config, f)


def updateSettings(update):
    loadsettings()
    #just create file in case

    with open('settings.cfg', 'r') as f:
        config = json.load(f)

    # edit the data
    for u in update:
        config[u[0]] = u[1]

    # write it back to the file
    with open('config.json', 'w') as f:
        json.dump(config, f)

def makesettings(updatetime , url , font, fontsize , model , slidetime):
    return {"updatetime": str(updatetime), "font": font,"fontsize": fontsize, "url": url, "model": str(model),
              "slidetime": str(slidetime)}


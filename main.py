
from GUI import GUIstart
from settings import loadSettings , updateSettings , log,logStart





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    settings = loadSettings()

    timer  = float(settings["slidetime"])
    model = int(settings["model"])
    font = settings["font"]
    url = settings["url"]
    updateTime = int(settings["updatetime"])
    """

    logStart()
    settings  = loadSettings()
    log("Settings loaded.")


    updatetime = int(settings["updatetime"])
    url = settings['url']
    font = settings['font']
    fontsize = int(settings['fontsize'])
    model = int(settings['model'])
    slidetime = float(settings['slidetime'])


    GUIstart( updatetime, url , font ,fontsize, model , slidetime)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from GUI import GUIstart
from settings import loadSettings , updateSettings
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    """
    settings = loadSettings()

    timer  = float(settings["slidetime"])
    model = int(settings["model"])
    font = settings["font"]
    url = settings["url"]
    updateTime = int(settings["updatetime"])
    """

    settings  = loadSettings()

    updatetime = int(settings["updatetime"])
    url = settings['url']
    font = settings['font']
    fontsize = int(settings['fontsize'])
    model = int(settings['model'])
    slidetime = float(settings['slidetime'])


    GUIstart(updatetime, url , font ,fontsize, model , slidetime)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

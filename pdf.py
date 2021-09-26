import os
from os import listdir
from os.path import isfile, join
import urllib.request, json



def getPDFS(path):
    files = os.listdir(path)
    for i in range (len(files)) :
        files[i] = path + files[i]
    return files


def getJSON(url_source):
    with urllib.request.urlopen(url_source) as url:
        data = json.loads(url.read().decode())
    return data

def decodeJSON(data):
    """
    TODO once json format is defined

    """

def updateDir(path , list):
    files = os.listdir(path)
    for f in files:
        if f not in list:
            os.remove(f)

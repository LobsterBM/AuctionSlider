import os
from os import listdir
from os.path import isfile, join
import urllib.request, json


pdf_path = "./pdf"


def download_file(download_url, filename):
    try:
        response = urllib.request.urlopen(download_url)
        file = open(filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        return
    except:
        global document_status
        document_status = False
        return


download_file(pdf_path, "Test")



connection_status = True
document_status = True
refreshing = False
def checkConnection(url):
    timeout = 5

    global connection_status
    try:

        request = requests.get(url, timeout=timeout)
        connection_status = True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        connection_status= False
    return

def getStatus():
    return connection_status,document_status,refreshing

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
    download all pdfs from json

    """

def updateDir(path , list):
    files = os.listdir(path)
    for f in files:
        if f not in list:
            os.remove(f)

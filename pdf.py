import os
from os import listdir
from os.path import isfile, join
import urllib.request, json
import shutil


pdf_path = "./pdf"


connection_status = True
document_status = True
refreshing = False

def serverUpdate(url):
    global refreshing
    refreshing = True

    global connection_status
    if checkConnection(url) != True:
        connection_status = False
        return None

    connection_status = True

    data = getJSON(url)

    pdf_list = decodeJSON(data)

    global document_status

    for e in pdf_list:
        try:
            download_file(e.url , e.title , pdf_path+"_temp")
        except:
            document_status = False
            return None
    document_status = True

    if fileTransfer() == False:
        return None
    refreshing = False
    return pdf_list









def download_file(download_url, filename , path):
    try:
        if os.path.exists(pdf_path+"_temp") == False:
            os.mkdir(pdf_path+"_temp")
        response = urllib.request.urlopen(download_url)
        file = open(path +"/"+ filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        return
    except:
        global document_status
        document_status = False
        return






def checkConnection(url):
    timeout = 5

    global connection_status
    try:

        response = urllib.request.urlopen("http://google.com")
        connection_status = True
        return True
    except :
        print("No internet connection.")
        connection_status= False
        return False
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
    pdf_list = []
    for d in data["files"] :
        pdfurl = d["url"]
        title = d['title']
        comment = d['comment']
        status = d['status']
        pdf_obj = PDFobject(pdfurl,title,comment,status)
        pdf_list.append(pdf_obj)
    return pdf_list


def fileTransfer():
    if os.path.exists(pdf_path+"_old"):

        shutil.rmtree(pdf_path+"_old", ignore_errors=True)
        #os.rmdir(pdf_path+"_old")
    try:
        if os.path.exists(pdf_path+"_temp") == False:
            return False
        if os.path.exists(pdf_path ):
            os.rename(pdf_path , pdf_path+"_old")
        os.rename(pdf_path+'_temp' , pdf_path)
        return True
    except:
        return False

def goBack():
    if os.path.exists(pdf_path+"_old"):
        os.rename(pdf_path+"_old" , pdf_path)




def updateDir(path , list):
    files = os.listdir(path)
    for f in files:
        if f not in list:
            os.remove(f)

class PDFobject :
    def __init__(self , url , title , comment , status):
        self.url = url
        self.title = title
        self.comment = comment
        self.status = status
        self.path = pdf_path+"/"+title+".pdf"

    def downloadPDF(self , path):

        download_file(self.url, self.title , path)

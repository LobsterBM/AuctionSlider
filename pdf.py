import os
from os import listdir
from os.path import isfile, join
import urllib.request, json
import shutil
from settings import log


pdf_path = "./pdf"


connection_status = True
document_status = True
refreshing = False




def serverUpdate(url):
    global refreshing
    refreshing = True

    global connection_status
    if checkConnection() != True:
        connection_status = False


    global document_status
    if checkServer(url) != True:
        document_status = False


    connection_status = True

    data = getJSON(url)

    if data == None :
        #try to use current PDF files , else return None
        log("Unable to get new data from server , using preexisting files if available.")
        pdf_list = current_PDF()
        refreshing = False
        if len(pdf_list) == 0 :
            log("There are no preexisting files.")
        return pdf_list

    else:
        pdf_list = decodeJSON(data)

    if pdf_list == None :
        return None

    for e in pdf_list:
        try:
            download_file(e.url , e.title , pdf_path+"_temp")
            document_status = True
        except:
            document_status = False
            #don't return None in case pdfs already exist in pdf location


    fileTransfer()
    refreshing = False
    return pdf_list






def current_PDF():
    global pdf_path
    if os.path.exists(pdf_path) == False :
        return None
    files = os.listdir(pdf_path)
    pdf_list = []
    for i in range (len(files)) :
        #files[i] = pdf_path + files[i]
        #the [:-4] is to remove the ".pdf" extension to make it compatible with the PDF object handler
        pdf_list.append(PDFobject("",files[i][:-4] , "",""))
    return pdf_list






def download_file(download_url, filename , path):
    log("Downloading file : " + download_url)
    try:
        if os.path.exists(pdf_path+"_temp") == False:
            os.mkdir(pdf_path+"_temp")
        response = urllib.request.urlopen(download_url)
        file = open(path +"/"+ filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        log("Download succeeded.")
        return
    except:
        global document_status
        document_status = False
        log("Download failed.")
        return






def checkConnection():
    timeout = 5

    global connection_status
    try:

        response = urllib.request.urlopen("http://google.com")
        connection_status = True
        return True
    except :
        log("Could not connect to the internet.")
        connection_status= False
        return False
    return

def checkServer(url):
    timeout = 5

    global connection_status
    try:

        response = urllib.request.urlopen(url)
        connection_status = True
        return True
    except :
        log("Could not connect to the server with url : " + url)
        connection_status= False
        return False
    return

def getStatus():
    checkConnection()
    return connection_status,document_status,refreshing

def getPDFS(path):
    files = os.listdir(path)
    for i in range (len(files)) :
        files[i] = path + files[i]
    return files


def getJSON(url_source):
    log("Fetching json from server.")
    try:
        with urllib.request.urlopen(url_source) as url:
            data = json.loads(url.read().decode())
        return data
    except:
        log("Error while fetching json from server ")
        return None

def decodeJSON(data):
    log("Decoding JSON")
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
    log("Updating new PDF directory")
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

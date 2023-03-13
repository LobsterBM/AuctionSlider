import threading
import time
from tkinter import *
from PIL import Image,ImageTk , ImageDraw , ImageFont
from pdf2image import convert_from_path
from screeninfo import get_monitors
from pdf import getPDFS , checkConnection , getStatus , serverUpdate , checkServer
from settings import log
slideinterrupt = False

fontsize = 15
slidefont = "./fonts/OpenSans-Semibold.ttf"




def getResolution():
    monitors =get_monitors()
    for m in monitors:
        if m.is_primary == True:
            width = (m.width)
            height = (m.height)
            return width,height

    width = (monitors[0].width)
    height = (monitors[0].height)

    return width, height

def updateSlides(data):
    if data == None :
        return None
    slides = []
    for d in data:
        conv = getSlides(d.path)
        #DO text
        #reformat d.comment to replace \r \n with \n
        d.comment = d.comment.replace("\r" , "")
        text = d.title + "\n" + d.comment + "\n" + d.status
        for e in conv :
            slides.append([e,  text])
    return slides




def refreshDB(url):
    data = serverUpdate(url)
    if data == None:
        return None
    slides = updateSlides(data)
    return slides



    #slide_list = makeSlides(slides, gui)


"""

def transparentText( alpha , fill , x1 , x2 , y1 , y2):
    canvas = Canvas(width = 500 , height = 150 )
    image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
    images.append(ImageTk.PhotoImage(image))
    canvas.create_image(x1, y1, image=images[-1], anchor='nw')

"""


def getSlides(location):
    pages = convert_from_path(location)
    images=[]
    for i in range (len(pages)):
        images.append(pages[i])
    return images

def multiplePages(pages , photos , pdf):
    for i in range(len(pages)):
        photos.append(ImageTk.PhotoImage(pages[i]))
    # Adding all the images to the text widget
    for photo in photos:
        pdf.image_create(END, image=photo)

        # For Seperating the pages
        pdf.insert(END, '\n\n')

def checkPDFS():
    return getPDFS("./pdf/")

def makeSlides(slides,gui):
    pos = 0
    slide_list =[]
    for s in slides:
        slide = Slide(s[0], s[1], gui , 0)
        pos +=1
        slide_list.append(slide)
    return slide_list
# TODO black screen on each update
# TODO slide each pdf right

# updates the list to cycle through the list
def nextSlides(slideList, gui ):
    if len(slideList) == 0 :
        return slideList

    
    gui.updateScreenSlides(slideList[0] , len(slideList))
    slideList = slideList[1:]+slideList[:1]


    gui.canvas.delete("all")

    gui.onscreen
    for s in gui.onscreen :
        s.show_slide()

    gui.root.update()


    return slideList



def updateIcons(gui, connection_canvas , document_canvas):
    connection , document = getStatus
    if connection:
        connection_canvas.delete("all")
    else:
        return
    if document :
        document_canvas.delete("all")
    else:
        return

def showIcon(image , gui , pos):
    w = gui.width
    h = gui.height
    canvas = gui.canvas
    canvas.pack()
    canvas.configure(background="black")
    imgWidth , imgHeight = image.size

    ratio = min((w/30) / imgWidth, (w/30) / imgHeight)
    imgWidth = int(imgWidth * ratio)
    imgHeight = int(imgHeight * ratio)


    image = image.resize((int(imgWidth),int(imgHeight)) , Image.ANTIALIAS)
    img_show = ImageTk.PhotoImage(image)
    imgsprite = canvas.create_image(w - (w/(10*pos)) , h - (h/(10*pos)) , image =img_show )
    gui.root.update()



def GUIstart(updatetime, url , newfont ,newfontsize, model , slidetime):

    log("Starting GUI")

    global slidefont
    global fontsize
    slidefont = newfont
    fontsize = newfontsize


    gui = GUIinstance(0,0,['fullscreen'], 3, "")
    root = gui.root
    root.config(cursor = "none")

    log("importing icons")
    try :
        connectionImage = Image.open("./icons/wifi.png")
        documentImage = Image.open("./icons/document.png")
        refreshImage = Image.open("./icons/refresh.png")
    except:
        log("Error importing Icons")
        return



    def exitKey(e):
        root.destroy()
    root.bind('<Escape>' , lambda e : exitKey(e))




    def slideThread(slide_list ,timer):


        #run these lines every time server is refreshed

        #timer *=60 #convert to minutes
        loops = timer/slidetime
        connectionStatus , documentStatus, refreshStatus = getStatus()
        if len(slide_list) <= 2 :
            gui.onscreen = []
        
        while  loops  > 0 :

            slide_list = nextSlides(slide_list , gui )

            if (documentStatus == False and connectionStatus == True):
                showIcon(documentImage, gui, 2)
            if (connectionStatus == False):
                showIcon(connectionImage, gui, 2)

            #gui.root.update()
            #connectionStatus,documentStatus,refreshStatus = getStatus()
            time.sleep(slidetime)
            loops -= 1
        #    print("loop : " ,loops)


    #first refresh

    log("Initial database refresh")
    data = refreshDB(url)

    if data == None :
        log("Could not refresh data , using existing sources if available ")

    #check if connection is up , check if document fetch works , add text message and loop with a refresh every minute
    #add to log

    while data == None :
        gui.canvas.delete("all")
        error_text = "Erreur :"
        if(checkConnection() == False ) :
            error_text += " pas de connection internet."
            showIcon(connectionImage, gui , 2)
        elif (checkServer(url) == False) :
            error_text += " impossible de récuperer les fichiers du serveur."
            showIcon(documentImage, gui , 2)

        canvas = gui.canvas
        canvas.pack()
        canvas.create_text(100, 280, text=error_text , font = (slidefont, fontsize*2) , fill = "white")
        #finally add text and loop
        #gui.root.update()
        data = refreshDB(url)
        time.sleep(5)
        log("Attempting to refresh the database again.")



    log("Initializing slideshow")

    while True:
        #slides = updateSlides(data)
        log("Making slides")
        slide_list = makeSlides(data,gui)

        log("Starting slideshow")
        slideThread(slide_list, updatetime)

        log("Fetching new data from database.")
        new_data = refreshDB(url)
        if new_data == None:
            log("No new data was found.")
        else :
            data = new_data


    def refreshThread(url):
        return refreshDB(url)





    """
        TODO :
            * settings  in general
            * kill thread if needed
            * PDF download & json config 
            * error logging
            *refresh status 
        
    """

    root.mainloop()

class GUIinstance:
    def __init__(self, width , height , attrs , model , location):
        if width == 0 or height == 0:
            width , height = getResolution()

        self.width = width
        self.height = height

        #Creating new TK isntance

        self.root = Tk()

        self.root.geometry('' + str(width) + "x" + str(height))
        for attr in attrs :
            self.root.attributes('-'+attr, True)

        #model 3 pdfs at a  time or 6
        self.model = model

        if model == 3 :
            self.modelBlocks = [[0,0],[width/3 , 0] , [(width/3)*2 , 0] ]
            self.img_size = [width/3 , height]
        if model == 6:
            self.modelBlocks = [[0,0],[width/3 , 0] , [(width/3)*2 , 0] , [0,0],[width/3 , 0] , [(width/3)*2 , 0]   ]
            self.img_size = [width/3 , height/2]

        #directory of pdf files (or images)
        self.location = location

        self.root.update_idletasks()
        self.root.update()
        self.canvas = Canvas(self.root, width=width, height=height)
        self.onscreen = []

    def updateScreenSlides(self, slide , slidelength):

        if len(self.onscreen) < self.model :
            for i in range(len(self.onscreen)):
                self.onscreen[i].setPos(i)
                if slidelength == 1 and len(self.onscreen) > 0:
                    self.onscreen[0].setPos(1)
            if slide not in self.onscreen:
                if slidelength == 1 :
                    slide.setPos(1)
                    self.onscreen = [slide]
                    return
                self.onscreen = [slide] + self.onscreen
            
        else:
            if slide not in self.onscreen:
                self.onscreen  = [slide]+self.onscreen[:-1]
            for i in range(len(self.onscreen)):
                self.onscreen[i].setPos(i)
                if slidelength == 1 :
                    self.onscreen[0].setPos(1)
            
            
            



class Slide:
    def __init__(self, image , text , gui , position):
        self.image = image
        self.text = text
        self.gui= gui
        self.position = position % self.gui.model
        self.x = self.gui.modelBlocks[self.position][0]
        self.y = self.gui.modelBlocks[self.position][1]
        self.image_shown = None


    def getPos(self):
        return self.position

    def movePos(self):
        self.position = (self.position+1) % self.gui.model

    def setPos(self, i):
        self.position = i % self.gui.model

    def show_slide(self):
        pilImage = self.image
        w=self.gui.width
        h=self.gui.height
        canvas = self.gui.canvas
        canvas.pack()
        canvas.configure(background='black')
        imgWidth, imgHeight = pilImage.size
        # resize photo to full screen
        #ratio = min(w / imgWidth, h / imgHeight)
        ratio = min(self.gui.img_size[0] / imgWidth, self.gui.img_size[1] / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        #self.image = ImageTk.PhotoImage(pilImage)



        model3 = [[-imgWidth , 0] , [0,0] , [imgWidth , 0]]
        model6 = [[-imgWidth , -imgHeight] , [0,-imgHeight] , [imgWidth , -imgHeight],[-imgWidth , imgHeight ] , [0,imgHeight] , [imgWidth , imgHeight]]


        if self.text != None and self.text != "":
            #Transparent Rectangle
            draw = ImageDraw.Draw(pilImage, "RGBA")

            font = ImageFont.truetype(slidefont, fontsize)
            draw.text((10, 10), self.text, (0, 0, 0) , font = font)

            text_size = font.getsize(self.text)

            #get lines of text for rectangle height
            lines = 1
            for c in self.text :
                if c == '\n' :
                    lines +=1





            rheight =(( text_size[1] ) * lines) +20
            if self.gui.model == 3 :
                draw.rectangle(((0, 0), (w/3, rheight)), fill=(100, 100, 100, 127))
                draw.rectangle(((0, 0), (w/3, rheight)), outline=(0, 0, 0, 127), width=2)


            #font = ImageFont.truetype("sans-serif.ttf", 16)
            # draw.text((x, y),"Sample Text",(r,g,b))


        self.image_shown = ImageTk.PhotoImage(pilImage)



        imagesprite = canvas.create_image((w / 2) + model3[self.position][0], h / 2 + model3[self.position][1], image=self.image_shown)
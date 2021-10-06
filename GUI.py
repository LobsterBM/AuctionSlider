import threading
import time
from tkinter import *
from PIL import Image,ImageTk , ImageDraw , ImageFont
from pdf2image import convert_from_path
from screeninfo import get_monitors
from pdf import getPDFS , checkConnection , getStatus


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

def updateSlides(path):
    files  = checkPDFS()
    slides = []
    for f in files:
        conv = getSlides(f)
        for e in conv:
            slides.append(e)
    return slides



def transparentText( alpha , fill , x1 , x2 , y1 , y2):
    canvas = Canvas(width = 500 , height = 150 )
    image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
    images.append(ImageTk.PhotoImage(image))
    canvas.create_image(x1, y1, image=images[-1], anchor='nw')


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
        slide = Slide(s, "sample text" + str(pos), gui , 0)
        pos +=1
        slide_list.append(slide)
    return slide_list
# TODO black screen on each update
# TODO slide each pdf right

# updates the list to cycle through the list
def nextSlides(slideList, gui):
    if len(slideList) == 0 :
        return slideList
    gui.updateScreenSlides(slideList[0])
    slideList = slideList[1:]+slideList[:1]

    gui.canvas.delete("all")

    onscreen = gui.onscreen
    for s in onscreen :
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



def GUIstart():

    files = checkPDFS()
    gui = GUIinstance(0,0,['fullscreen'], 3, "")
    root = gui.root
    root.config(cursor = "none")
    width = gui.width
    height = gui.height

    def exitKey(e):
        root.destroy()
    root.bind('<Escape>' , lambda e : exitKey(e))


    connectionImage = Image.open("./icons/wifi.png")
    documentImage = Image.open("./icons/document.png")
    refreshImage = Image.open("./icons/refresh.png")


    def slideThread():

        #run these lines every time server is refreshed
        slides = updateSlides("")
        slide_list = makeSlides(slides,gui)

        connectionStatus , documentStatus, refreshStatus = True,True , False
        while True :
            connectionStatus,documentStatus,refreshStatus = getStatus()
            slide_list = nextSlides(slide_list , gui)
            if (documentStatus == False):
                showIcon(documentImage, gui, 2)
            if (connectionStatus == False):
                showIcon(connectionImage, gui, 2)
            if(refreshStatus):
                showIcon(refreshImage , gui , 2)
            time.sleep(1)

    while True:
        slide_thread = threading.Thread(target=slideThread())
        slide_thread.start()
        time.sleep(600)
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

    def updateScreenSlides(self, slide ):
        if len(self.onscreen) < self.model :
            for i in range(len(self.onscreen)):
                self.onscreen[i].setPos(i)
            self.onscreen = [slide] + self.onscreen
        else:
            self.onscreen  = [slide]+self.onscreen[:-1]
            for i in range(len(self.onscreen)):
                self.onscreen[i].setPos(i)



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
            if self.gui.model == 3 :
                draw.rectangle(((0, 0), (w/3, 70)), fill=(100, 100, 100, 127))
                draw.rectangle(((0, 0), (w/3, 70)), outline=(0, 0, 0, 127), width=2)


            #font = ImageFont.truetype("sans-serif.ttf", 16)
            # draw.text((x, y),"Sample Text",(r,g,b))

            font = ImageFont.truetype("./fonts/OpenSans-Semibold.ttf", 35)
            draw.text((10, 10), self.text, (0, 0, 0) , font = font)

        self.image_shown = ImageTk.PhotoImage(pilImage)



        imagesprite = canvas.create_image((w / 2) + model3[self.position][0], h / 2 + model3[self.position][1], image=self.image_shown)
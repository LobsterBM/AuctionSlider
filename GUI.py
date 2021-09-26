import time
from tkinter import *
from PIL import Image,ImageTk , ImageDraw , ImageFont
from pdf2image import convert_from_path
from screeninfo import get_monitors
from pdf import getPDFS


def getResolution():
    monitors =get_monitors()
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
        slide = Slide(s, "", gui , pos)
        pos +=1
        slide_list.append(slide)
    return slide_list


def GUIstart():

    files = checkPDFS()
    gui = GUIinstance(0,0,['fullscreen'], 3, "")
    root = gui.root
    width = gui.width
    height = gui.height

    #run these lines every time server is refreshed
    slides = updateSlides("")
    slide_list = makeSlides(slides,gui)




    for s in slide_list:
        s.show_slide()
        root.update()
        time.sleep(1.5)



    """
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    canvas.configure(background='black')


    # Storing the converted images into list
    exit_button = Button(root, text="Exit", command=root.destroy )
    exit_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    button1_window = canvas.create_window(10, 10, anchor=NW, window=exit_button)
    root.update()"""

    #transparentText(0.9 , 'blue', 50 , 100 , 50,100)
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

class Slide:
    def __init__(self, image , text , gui , position):
        self.image = image
        self.text = text
        self.gui= gui
        self.position = position % self.gui.model
        self.x = self.gui.modelBlocks[self.position][0]
        self.y = self.gui.modelBlocks[self.position][1]

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

        #Transparent Rectangle
        draw = ImageDraw.Draw(pilImage, "RGBA")
        draw.rectangle(((10, 10), (100, 70)), fill=(200, 100, 0, 127))
        draw.rectangle(((10, 10), (100, 70)), outline=(0, 0, 0, 127), width=3)

        #font = ImageFont.truetype("sans-serif.ttf", 16)
        # draw.text((x, y),"Sample Text",(r,g,b))

        font = ImageFont.truetype("./fonts/OpenSans-Semibold.ttf", 35)
        draw.text((10, 10), "Sample Text", (0, 0, 0) , font = font)

        self.image = ImageTk.PhotoImage(pilImage)

        model3 = [[-imgWidth , 0] , [0,0] , [imgWidth , 0]]
        model6 = [[-imgWidth , -imgHeight] , [0,-imgHeight] , [imgWidth , -imgHeight],[-imgWidth , imgHeight ] , [0,imgHeight] , [imgWidth , imgHeight]]


        imagesprite = canvas.create_image((w / 2) + model3[self.position][0], h / 2 + model3[self.position][1], image=self.image)
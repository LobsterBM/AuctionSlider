from tkinter import *
from PIL import Image,ImageTk
from pdf2image import convert_from_path
from screeninfo import get_monitors
def getResolution():
    monitors =get_monitors()
    width = (monitors[0].width)
    height = (monitors[0].height)
    return width, height


def GUIstart():
    width , height = getResolution()
    root = Tk()
    root.geometry(''+str(width)+"x"+str(height))
    root.attributes('-fullscreen', True)
    # Creating the frame for PDF Viewer
    # pdf_frame = Frame(root).pack(fill=NONE, expand=1)


    # Adding Scrollbar to the PDF frame
    #scrol_y = Scrollbar(pdf_frame, orient=VERTICAL)
    # Adding text widget for inserting images
    #pdf = Text(pdf_frame, yscrollcommand=scrol_y.set, bg="grey")
    #pdf = Text(pdf_frame, bg="black")
    # Setting the scrollbar to the right side
    #scrol_y.pack(side=RIGHT, fill=Y)
    #scrol_y.config(command=pdf.yview)
    # Finally packing the text widget
    #pdf.pack(fill=BOTH, expand=1, side= TOP)
    # Here the PDF is converted to list of images
    pages = convert_from_path('foobar.pdf')
    # Empty list for storing images
    photos = []
    pilImage = pages[0]
    w = width
    h = height
    canvas = Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    # resize photo to full screen
    ratio = min(w / imgWidth, h / imgHeight)
    imgWidth = int(imgWidth * ratio)
    imgHeight = int(imgHeight * ratio)
    pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w / 2, h / 2, image=image)
    root.update_idletasks()
    root.update()
    # Storing the converted images into list
    """
    for i in range(len(pages)):
        photos.append(ImageTk.PhotoImage(pages[i]))
    # Adding all the images to the text widget
    for photo in photos:
        pdf.image_create(END, image=photo)

        # For Seperating the pages
        pdf.insert(END, '\n\n')
    # Ending of mainloop"""
    exit_button = Button(root, text="Exit", command=root.destroy )
    exit_button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    button1_window = canvas.create_window(10, 10, anchor=NW, window=exit_button)

    root.mainloop()
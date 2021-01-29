from tkinter import *
#import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO

#root = tk.Tk()
#img_url = "http://www.universeofsymbolism.com/images/ram-spirit-animal.jpg"
#response = requests.get(img_url)
#img_data = response.content
#img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
#panel = tk.Label(root, image=img)
#panel.grid(row=0, column=1)
#panel.pack(side="bottom", fill="both", expand="yes")


window = Tk()
img_url = "http://www.universeofsymbolism.com/images/ram-spirit-animal.jpg"
response = requests.get(img_url)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel = Label(window, image=img)
panel.grid(row=0, column=1)

    #im = Image.open(BytesIO(raw_data))
    #print(im.size)
    #photo = ImageTk.PhotoImage(im)
    #photo = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
    #print(photo)
    #label1 = Label(window, image=photo)
    #label1.grid(row=0, column=1, sticky=W)

    #fin=urlopen(yt.thumbnail_url)
    #s=io.BytesIO(fin.read())
    #pil_image= Image.open(s)
    #print (pil_image.size)
    #tk_image = ImageTk.PhotoImage(pil_image)
    #label1 = Label(window, image = pil_image)
    #label1.grid(row=0, column=1, sticky=W)

    #response = requests.get(yt.thumbnail_url)
    #img_data = response.content
    #img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    #panel = Label(window, image=img)
    #panel.grid(row=0, column=1, sticky=W)

    #raw = urlopen(yt.thumbnail_url).read()
    #img = Image.open(io.BytesIO(raw))
    #ThumbPrvw = ImageTk.PhotoImage(img)
    #label1 = Label(window, image = ThumbPrvw)
    #label1.grid(row=0, column=1, sticky=W)



window.mainloop()

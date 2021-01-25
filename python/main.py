from tkinter import *
from pytube import YouTube

def dlit():
    url = textbox.get()
    output.delete(0.0, END) #first line first character and delete til end
    #I need to include a check on the text entered to ensure it has a www.youtube.com
    yt = YouTube(url)
    #yt = YouTube('https://www.youtube.com/watch?v=yUdxHAhj8l8')
    sort = yt.streams
    output.insert(END, sort)

def close():
    window.destroy()
    exit()


window = Tk()
window.title("Youtube Downloader")
window.configure(background = "black")

check = IntVar()

logo = PhotoImage(file = "../assets/hacker.gif")
Label (window, image = logo, bg = "black") .grid(row = 0, column = 0, sticky = W)

Label (window, text="Please enter the video URL:", bg = "black", fg = "white", font = "non 12 bold") .grid(row = 1, column = 0, sticky = W)

textbox = Entry(window, width = 50, bg = "white")
textbox.grid(row = 2, column = 0, sticky = W)

audiocheckbox = Checkbutton(window, text = "Filter - Audio Only", bg = "black", fg = "white", variable = check)
audiocheckbox.grid(row = 3, column = 1, sticky = W)
#audiocheckbox.pack()

Button(window, text = "List Streams ", width = 12, command = dlit) .grid(row = 3, column = 0, sticky = W)
Button(window, text = "Close", width = 10, command = close) .grid(row = 6, column = 0, sticky = E)

output = Text(window, width = 100, height = 20, wrap = WORD, background = "white")
output.grid(row = 5, column = 0, columnspan = 2, sticky = W)

window.mainloop()

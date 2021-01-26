from tkinter import *
from pytube import YouTube
from pytube.helpers import safe_filename

def ListStreams():
    url = TextBox.get()
    #I need to include a check on the text entered to ensure it has a www.youtube.com
    yt = YouTube(url)
    #yt = YouTube('https://www.youtube.com/watch?v=yUdxHAhj8l8')
    output.delete(0.0, END) #delete first character on the first line til the end of the textbox
    audio_flag = check.get()
    #StreamList = yt.streams
    for stream in yt.streams.filter(only_audio=audio_flag):
        if audio_flag:
            StreamList = f'itag: {stream.itag} Codec: {stream.audio_codec} BitRate: {stream.abr} File Type: {stream.mime_type.split("/")[1]}\n'
            output.insert(END, StreamList)
        else:
                if stream.mime_type.split("/")[1] == "mp4":# and (stream.resolution == "720p" or stream.resolution == "1080p"):
                    StreamList = f'itag: {stream.itag} Resolution: {stream.resolution} FPS: {stream.fps} File Type: {stream.mime_type.split("/")[1]}\n'
                    output.insert(END, StreamList)
    print(audio_flag) #for debugging purposes

def close():
    window.destroy()
    exit()


window = Tk()
window.title("Youtube Downloader by Alykes")
window.configure(background = "grey")

check = IntVar()
#check.set(True)

logo = PhotoImage(file = "../assets/hacker.gif")
Label (window, image = logo, bg = "grey") .grid(row = 0, column = 0, sticky = W)

Label (window, text="Please enter the video URL:", bg = "grey", fg = "black", font = "none 12") .grid(row = 1, column = 0, sticky = W)

TextBox = Entry(window, width = 70, bg = "white")
TextBox.grid(row = 2, column = 0, sticky = W)

AudioCheckbox = Checkbutton(window, text = "Audio Only", bg = "grey", fg = "black", variable = check, onvalue = 1, offvalue = 0)
AudioCheckbox.grid(row = 3, column = 1, sticky = W)
#AudioCheckbox.pack()

Button(window, text = "List Streams ", width = 12, command = ListStreams) .grid(row = 3, column = 0, sticky = W)
Button(window, text = "Close", width = 10, command = close) .grid(row = 7, column = 1, sticky = E)

output = Text(window, width = 70, height = 20, wrap = WORD, background = "white")
output.grid(row = 5, column = 0, columnspan = 2, sticky = W)

window.mainloop()

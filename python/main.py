from tkinter import *
from pytube import YouTube
from pytube.helpers import safe_filename

def ListStreams():
    url.set(TextBox.get())
    #I need to include a check on the text entered to ensure it has a www.youtube.com
    yt = YouTube(url.get())
    #yt = YouTube('https://www.youtube.com/watch?v=yUdxHAhj8l8')
    streamLB.delete(0, END)

    audio_flag = check.get()

    for stream in yt.streams.filter(only_audio=audio_flag):
        if audio_flag:
            StreamItem = f'itag: {stream.itag} Codec: {stream.audio_codec} BitRate: {stream.abr} File Type: {stream.mime_type.split("/")[1]}\n'
            streamLB.insert(END, StreamItem)
        else:
                if stream.mime_type.split("/")[1] == "mp4":# and (stream.resolution == "720p" or stream.resolution == "1080p"):
                    StreamItem = f'itag: {stream.itag} Resolution: {stream.resolution} FPS: {stream.fps} File Type: {stream.mime_type.split("/")[1]}\n'
                    streamLB.insert(END, StreamItem)
    print(audio_flag) #for debugging purposes

def selection(mouse_event):
    item = streamLB.get(ANCHOR)
    arr = item.split()
    itag = int(arr[1])
    print(item) #for debugging purposes
    chosen.set(itag)

def Download():
    print('Downloading: ', chosen.get())
    YouTube(url.get()).streams.get_by_itag(chosen.get()).download(output_path=".", filename="test")


def close():
    window.destroy()
    exit()

window = Tk()
window.title("Youtube Downloader by Alykes")
window.configure(background = "grey")

check = IntVar()
chosen = StringVar()
url = StringVar()

logo = PhotoImage(file = "../assets/hacker.gif")
Label (window, image = logo, bg = "grey") .grid(row = 0, column = 0, sticky = W)

Label (window, text="Please enter the video URL:", bg = "grey", fg = "black", font = "none 12") .grid(row = 1, column = 0, sticky = W)

TextBox = Entry(window, width = 70, bg = "white")
TextBox.grid(row = 2, column = 0, sticky = W)

AudioCheckbox = Checkbutton(window, text = "Audio Only", bg = "grey", fg = "black", variable = check, onvalue = 1, offvalue = 0)
AudioCheckbox.grid(row = 3, column = 1, sticky = W)

Button(window, text = "List Streams ", width = 12, command = ListStreams, pady = 2) .grid(row = 3, column = 0, sticky = W)
Button(window, text = "Download", width = 10, command = Download) .grid(row = 7, column = 0, sticky = W)
Button(window, text = "Close", width = 10, command = close) .grid(row = 7, column = 1, sticky = E)

streamLB = Listbox(window, width=80)
streamLB.grid(row = 5, column = 0, columnspan = 2, sticky = W)

streamLB.bind("<ButtonRelease-1>", selection)

window.mainloop()

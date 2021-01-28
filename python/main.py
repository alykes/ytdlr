from tkinter import filedialog
from tkinter import *
from pytube import YouTube
from PIL import ImageTk, Image
#from pytube.helpers import safe_filename

def ListStreams():
    url.set(TextBox.get())
    #I need to include a check on the text entered to ensure it has a www.youtube.com
    yt = YouTube(url.get())
    #yt = YouTube('https://www.youtube.com/watch?v=yUdxHAhj8l8')
    #ytthumb="https://i.ytimg.com/vi/yUdxHAhj8l8/mqdefault.jpg"
    streamLB.delete(0, END)

    ytThumb = yt.thumbnail_url

    audio_flag = check.get()

    for stream in yt.streams.filter(only_audio=audio_flag):
        if audio_flag:
            StreamItem = f'itag: {stream.itag} Codec: {stream.audio_codec} BitRate: {stream.abr} File Type: {stream.mime_type.split("/")[1]}\n'
            streamLB.insert(END, StreamItem)
        else:
                if stream.mime_type.split("/")[1]:# == "mp4":# and (stream.resolution == "720p" or stream.resolution == "1080p"):
                    StreamItem = f'itag: {stream.itag} Resolution: {stream.resolution} FPS: {stream.fps} File Type: {stream.mime_type.split("/")[1]}\n'
                    streamLB.insert(END, StreamItem)
    print(audio_flag) #for debugging purposes

def selection(mouse_event):
    item = streamLB.get(ANCHOR)
    arr = item.split()
    itag = int(arr[1])
    print(item) #for debugging purposes
    chosen.set(itag)

def Browse():
    print("Please select the download directory")
    DownloadPath = filedialog.askdirectory()
    TextBox2.configure(state='normal')
    TextBox2.delete(0, END)
    TextBox2.insert(END, DownloadPath)
    TextBox2.configure(state = 'disabled')

    print(DownloadPath)


def Download():
    print('Downloading: ', chosen.get())

    #if len(TextBox2.get()) == 0:
    #    output_path = '.'
    #    TextBox2.configure(state='normal')
    #    TextBox2.insert(END, ".")
    #    TextBox2.configure(state = 'disabled')
    #else:
    #    output_path = TextBox2.get()
    ytDL = YouTube(url.get())
    fname = ytDL.title
    ytDL.streams.get_by_itag(chosen.get()).download(output_path=TextBox2.get(), filename=fname)

def close():
    window.destroy()
    #exit()

window = Tk()
window.title("Youtube Downloader by Alykes")
window.configure(background = "lightgrey")

check = IntVar()
chosen = StringVar()
url = StringVar()

logo = PhotoImage(file = "../assets/hacker.gif")
Label (window, image = logo, bg = "lightgrey") .grid(row = 0, column = 0, sticky = W)

####
thumb = Image.open("../assets/mqdefault.jpg")
thumb = thumb.resize((150, 100), Image.ANTIALIAS)
ytthumb = ImageTk.PhotoImage(thumb)
####
Label (window, image = ytthumb, bg = "lightgrey", width = 180, height = 100) .grid(row = 6, column = 2)

Label (window, text="YouTube URL: ", bg = "lightgrey", fg = "black", font = "none 10") .grid(row = 1, column = 0, sticky = W)
TextBox = Entry(window, width = 70, bg = "white")
TextBox.grid(row = 1, column = 1, sticky = W)

Label (window, text="Download Folder:  ", bg = "lightgrey", fg = "black", font = "none 10") .grid(row = 2, column = 0, sticky = W)
TextBox2 = Entry(window, width = 70, bg = "white")#, state = 'disabled')
TextBox2.grid(row = 2, column = 1, sticky = W)
TextBox2.insert(0, '.')
TextBox2.configure(state = "disabled")

AudioCheckbox = Checkbutton(window, text = "Audio Only", bg = "lightgrey", fg = "black", variable = check, onvalue = 1, offvalue = 0)
AudioCheckbox.grid(row = 4, column = 1, sticky = W)

Button(window, text = "List Streams ", width = 12, command = ListStreams) .grid(row = 4, column = 0, sticky = W)
Button(window, text = "Browse", width = 12, command = Browse) .grid(row = 2, column = 2)
Button(window, text = "Download", width = 10, command = Download) .grid(row = 8, column = 0, sticky = W)
Button(window, text = "Close", width = 10, command = close) .grid(row = 8, column = 2, sticky = E)

streamLB = Listbox(window, width=80)
streamLB.grid(row = 6, column = 0, columnspan = 2, sticky = W)

streamLB.bind("<ButtonRelease-1>", selection)

window.mainloop()

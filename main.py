from io import BytesIO
import os
import requests
from tkinter import *
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning
from pytube import YouTube
from pytube.cli import on_progress
from PIL import ImageTk, Image
from urllib.request import urlopen


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def list_streams():
    chosen.set(0)
    url.set(TextBox.get())

    if "www.youtube.com/watch?v=" or "youtu.be" in url.get():
        try:
            yt = YouTube(url.get())
        except:
            showwarning("Window", "WARNING: Unable to retrieve streams. Please check the URL.")
            return None
    #yt = YouTube('https://www.youtube.com/watch?v=yUdxHAhj8l8')
    streamLB.delete(0, END)

    img_url = yt.thumbnail_url
    #img_url = "https://i.ytimg.com/vi/CRuOOxF-ENQ/maxresdefault.jpg"
    response = requests.get(img_url)
    img_data = response.content
    tmp_img = Image.open(BytesIO(img_data))
    resized = tmp_img.resize((180,120),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)

    PreviewThumb.configure(image=img)
    PreviewThumb.image=img

    TitleBox.configure(state='normal')
    TitleBox.delete(0, END)
    TitleBox.insert(END, yt.title)
    TitleBox.configure(state = 'disabled')

    audio_flag = checkAF.get()

    for stream in yt.streams.filter(only_audio = audio_flag):
        if audio_flag:
            stream_item = f'itag: {stream.itag} Codec: {stream.audio_codec} BitRate: {stream.abr} File Type: {stream.mime_type.split("/")[1]}\n'
            streamLB.insert(END, stream_item)
        elif stream.resolution != None:
                stream_item = f'itag: {stream.itag} Resolution: {stream.resolution} FPS: {stream.fps} File Type: {stream.mime_type.split("/")[1]}\n'
                streamLB.insert(END, stream_item)


def copy_pasta(mouse_event):
    if TextBox.get() != window.clipboard_get() and PastaCheck.get() == 0 and window.clipboard_get() != "":
        TextBox.delete(0, END)
        TextBox.insert(END, window.clipboard_get())


def selection(mouse_event):
    if streamLB.size() > 0:
        lb_item = streamLB.get(ANCHOR)
        arr = lb_item.split()
        itag = int(arr[1])

        chosen.set(itag)


def browse():
    download_path = filedialog.askdirectory()

    TextBox2.configure(state='normal')
    TextBox2.delete(0, END)
    TextBox2.insert(END, download_path)
    TextBox2.configure(state = 'disabled')


def download():
    if streamLB.size() > 0 and chosen.get() != 0:
        yt_dl = YouTube(url.get(), on_progress_callback=progress_update)
        fname = yt_dl.title
        try:
            yt_dl.streams.get_by_itag(chosen.get()).download(output_path = TextBox2.get(), filename = fname)
        except:
            showwarning("Window", "WARNING: Download did not complete!")
            return None

        showinfo("Window", "Download Completed!")


def progress_update(stream, chunk, bytes_remaining):
    ratio_complete = ((stream.filesize - bytes_remaining)/stream.filesize)
    progress_bar['value'] = ratio_complete
    window.update_idletasks()


def close():
    window.destroy()
    exit()


version = "1.2.4"
window = Tk()

#Window Title Bar Text
icon = PhotoImage(file = resource_path("./assets/003-download.png"))
window.iconphoto(False, icon)
WindowTitle = 'Youtube Downloader by Alykes - [' + version + ']'
window.title(string = WindowTitle)
window.configure(background = "lightgrey")

#Set up tkinter variables
checkAF = IntVar()
PastaCheck = IntVar()
chosen = IntVar()
url = StringVar()

#Window Logo Placeholder
logo = PhotoImage(file = resource_path("./assets/hacker.gif"))
Label (window, image = logo, bg = "lightgrey") .grid(row = 0, column = 0, sticky = W)

#Default Thumbnail preview (shameless plug)
thumb = Image.open(resource_path("./assets/mqdefault.jpg"))
thumb = thumb.resize((180, 120), Image.ANTIALIAS)
ytthumb = ImageTk.PhotoImage(thumb)

PreviewThumb = Label (window, bg = "lightgrey", image = ytthumb, relief = GROOVE, width = 180, height = 120)
PreviewThumb.grid(row = 6, column = 2, padx=10, pady=10)

#Window Labels and associated TextBoxes
Label (window, text="YouTube URL: ", bg = "lightgrey", fg = "black", font = "Tahoma 10") .grid(row = 1, column = 0, sticky = W)
TextBox = Entry(window, width = 70, bg = "white")
TextBox.grid(row = 1, column = 1, sticky = W)
TextBox.focus_set()

Label (window, text="Download Folder:  ", bg = "lightgrey", fg = "black", font = "Tahoma 10") .grid(row = 2, column = 0, sticky = W)
TextBox2 = Entry(window, width = 70, bg = "white")
TextBox2.grid(row = 2, column = 1, sticky = W)
TextBox2.insert(0, '.')
TextBox2.configure(state = "disabled")

TitleBox = Entry(window, width = 30, bg = "lightgrey")
TitleBox.grid(row = 7, column = 2, sticky = N)
TitleBox.configure(state = "disabled")

Label (window, text="Download Progress:", bg = "lightgrey", fg = "black", font = "Tahoma 10") .grid(row = 8, column = 0, sticky = W)

#Window CheckBoxes
PastaCheckbox = Checkbutton(window, text = "Disable Auto-Paste", bg = "lightgrey", fg = "black", variable = PastaCheck, onvalue = 1, offvalue = 0)
PastaCheckbox.grid(row = 1, column = 2, sticky = W)

AudioCheckbox = Checkbutton(window, text = "Audio Only", bg = "lightgrey", fg = "black", variable = checkAF, onvalue = 1, offvalue = 0)
AudioCheckbox.grid(row = 4, column = 1, sticky = W)

#Window buttons
Button(window, text = "List Streams ", width = 12, command = list_streams) .grid(row = 4, column = 0, padx=10, pady=5, sticky = W)
Button(window, text = "Browse", width = 12, command = browse) .grid(row = 2, column = 2, sticky = W)
Button(window, text = "Download", width = 10, command = download) .grid(row = 8, column = 2, padx=10, pady=10, sticky = W)
Button(window, text = "Close", width = 10, command = close) .grid(row = 8, column = 2, padx=10, pady=10, sticky = E)

#Window ListBox
streamLB = Listbox(window, width=88)
streamLB.grid(row = 6, column = 0, columnspan = 2, padx=10, pady=10, sticky = W)

#Progress Bar
progress_bar = ttk.Progressbar(window, orient = "horizontal", mode = "determinate", length = 425, maximum = 1, value = 0)
progress_bar.grid(row = 8, column = 1, sticky = W)

#Events
streamLB.bind("<ButtonRelease-1>", selection)
TextBox.bind("<ButtonRelease-1>", copy_pasta)
#TextBox.bind("<Return>", list_streams)

window.mainloop()

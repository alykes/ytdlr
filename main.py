import os
from io import BytesIO

import requests
from PIL import Image, ImageTk
from pytube import YouTube
from pytube.cli import on_progress
from tkinter import * # Tk, Label, Entry, Button, Listbox, Checkbutton, IntVar, StringVar, W, END, NORMAL, DISABLED
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning



def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    
    Parameters:
    relative_path (str): The relative path to the resource.
    
    Returns:
    str: The absolute path to the resource.
    """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        return None



def list_streams():
    """
    List available streams for the provided YouTube URL and update the UI elements.
    """
    chosen.set(0)
    url.set(TextBox.get())

    if "www.youtube.com/watch?v=" in url.get() or "youtu.be" in url.get():
        try:
            yt = YouTube(url.get())
        except Exception as e:
            showwarning("Window", f"WARNING: Unable to retrieve streams. Please check the URL. Error: {e}")
            return None

        streamLB.delete(0, END)

        # Update thumbnail
        img_url = yt.thumbnail_url
        response = requests.get(img_url)
        img_data = response.content
        tmp_img = Image.open(BytesIO(img_data))
        resized = tmp_img.resize((180, 120), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)

        PreviewThumb.configure(image=img)
        PreviewThumb.image = img

        # Update title
        TitleBox.configure(state=NORMAL)
        TitleBox.delete(0, END)
        TitleBox.insert(END, yt.title)
        TitleBox.configure(state=DISABLED)

        # List streams
        audio_flag = checkAF.get()
        streams = yt.streams.filter(only_audio=audio_flag)
        for stream in streams:
            if audio_flag:
                stream_item = (
                    f'itag: {stream.itag} Codec: {stream.audio_codec} '
                    f'BitRate: {stream.abr} File Type: {stream.mime_type.split("/")[1]}\n'
                )
            else:
                if stream.resolution:
                    stream_item = (
                        f'itag: {stream.itag} Resolution: {stream.resolution} '
                        f'FPS: {stream.fps} File Type: {stream.mime_type.split("/")[1]}\n'
                    )
            streamLB.insert(END, stream_item)


def copy_pasta(mouse_event):
    """
    Copy text from the clipboard to TextBox if conditions are met.
    """
    clipboard_content = window.clipboard_get()
    if (
        TextBox.get() != clipboard_content 
        and PastaCheck.get() == 0 
        and clipboard_content != ""
    ):
        TextBox.delete(0, END)
        TextBox.insert(END, clipboard_content)

def selection(mouse_event):
    """
    Update the chosen variable with the itag of the selected listbox item.
    """
    if streamLB.size() > 0:
        lb_item = streamLB.get(ANCHOR)
        arr = lb_item.split()
        itag = int(arr[1])
        chosen.set(itag)



def browse():
    """
    Open a dialog to select a directory and update the TextBox2 with the selected path.
    """
    download_path = filedialog.askdirectory()

    TextBox2.configure(state=NORMAL)
    TextBox2.delete(0, END)
    TextBox2.insert(END, download_path)
    TextBox2.configure(state=DISABLED)


def download():
    """
    Download the selected YouTube stream to the specified directory.
    """
    if streamLB.size() > 0 and chosen.get() != 0:
        yt_dl = YouTube(url.get(), on_progress_callback=progress_update)
        fname = yt_dl.title
        try:
            stream = yt_dl.streams.get_by_itag(chosen.get())
            output_path = TextBox2.get()
            stream.download(output_path=output_path, filename=fname)
            showinfo("Window", "Download Completed!")
        except Exception as e:
            showwarning("Window", f"WARNING: Download did not complete! Error: {e}")
            return None



def progress_update(stream, chunk, bytes_remaining):
    """
    Update the progress bar during the download process.
    """
    ratio_complete = (stream.filesize - bytes_remaining) / stream.filesize
    progress_bar['value'] = ratio_complete
    window.update_idletasks()

def close():
    """
    Close the application window.
    """
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

# Window Logo Placeholder
logo = PhotoImage(file=resource_path("./assets/hacker.gif"))
Label(window, image=logo, bg="lightgrey").grid(row=0, column=0, sticky=W)

# Default Thumbnail preview (shameless plug)
thumb = Image.open(resource_path("./assets/mqdefault.jpg"))
thumb = thumb.resize((180, 120), Image.ANTIALIAS)
ytthumb = ImageTk.PhotoImage(thumb)

PreviewThumb = Label(
    window, 
    bg="lightgrey", 
    image=ytthumb, 
    relief=GROOVE, 
    width=180, 
    height=120
)
PreviewThumb.grid(row=6, column=2, padx=10, pady=10)

# Window Labels and associated TextBoxes
Label(
    window, 
    text="YouTube URL:", 
    bg="lightgrey", 
    fg="black", 
    font="Tahoma 10"
).grid(row=1, column=0, sticky=W)

TextBox = Entry(window, width=70, bg="white")
TextBox.grid(row=1, column=1, sticky=W)
TextBox.focus_set()

Label(
    window, 
    text="Download Folder:", 
    bg="lightgrey", 
    fg="black", 
    font="Tahoma 10"
).grid(row=2, column=0, sticky=W)

TextBox2 = Entry(window, width=70, bg="white")
TextBox2.grid(row=2, column=1, sticky=W)
TextBox2.insert(0, '.')
TextBox2.configure(state="disabled")

TitleBox = Entry(window, width=30, bg="lightgrey")
TitleBox.grid(row=7, column=2, sticky=N)
TitleBox.configure(state="disabled")

Label(
    window, 
    text="Download Progress:", 
    bg="lightgrey", 
    fg="black", 
    font="Tahoma 10"
).grid(row=8, column=0, sticky=W)

# Window CheckBoxes
PastaCheckbox = Checkbutton(
    window,
    text="Disable Auto-Paste",
    bg="lightgrey",
    fg="black",
    variable=PastaCheck,
    onvalue=1,
    offvalue=0
)
PastaCheckbox.grid(row=1, column=2, sticky=W)

AudioCheckbox = Checkbutton(
    window,
    text="Audio Only",
    bg="lightgrey",
    fg="black",
    variable=checkAF,
    onvalue=1,
    offvalue=0
)
AudioCheckbox.grid(row=4, column=1, sticky=W)

# Create buttons
list_streams_button = Button(window, text="List Streams", width=12, command=list_streams)
browse_button = Button(window, text="Browse", width=12, command=browse)
download_button = Button(window, text="Download", width=10, command=download)
close_button = Button(window, text="Close", width=10, command=close)

# Configure grid layout
list_streams_button.grid(row=4, column=0, padx=10, pady=5, sticky=W)
browse_button.grid(row=2, column=2, sticky=W)
download_button.grid(row=8, column=2, padx=10, pady=10, sticky=W)
close_button.grid(row=8, column=2, padx=10, pady=10, sticky=E)

#Window ListBox
streamLB = Listbox(window, width=88)
streamLB.grid(row = 6, column = 0, columnspan = 2, padx=10, pady=10, sticky = W)

# Progress Bar
progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    mode="determinate",
    length=425,
    maximum=1,
    value=0
)
progress_bar.grid(row=8, column=1, sticky=W)

#Events
streamLB.bind("<ButtonRelease-1>", selection)
TextBox.bind("<ButtonRelease-1>", copy_pasta)
#TextBox.bind("<Return>", list_streams)

window.mainloop()

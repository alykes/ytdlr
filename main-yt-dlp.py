# Conversion to use yt-dlp made by claude (I didn't want to spend hours re-writing this whole thing! :D )

import os
from io import BytesIO
import sys
import yt_dlp
import requests
from PIL import Image, ImageTk
from tkinter import Tk, Label, Entry, Button, Listbox, Checkbutton, IntVar, StringVar, N, E, S, W, END, NORMAL, DISABLED, GROOVE, ANCHOR
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo, showwarning

def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        return None

def get_video_info(url):
    """
    Get video information using yt-dlp.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # Get full format information
        'format_sort': ['res:1080', 'ext:mp4:m4a', 'codec:h264:aac'],  # Add format sorting
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        raise Exception(f"Error extracting video info: {e}")

def list_streams():
    """
    List available streams for the provided YouTube URL and update the UI elements.
    """
    chosen.set(0)
    url.set(TextBox.get())

    if "youtube.com" in url.get() or "youtu.be" in url.get():
        try:
            video_info = get_video_info(url.get())
            
            streamLB.delete(0, END)

            # Update thumbnail
            img_url = video_info.get('thumbnail')
            response = requests.get(img_url)
            img_data = response.content
            tmp_img = Image.open(BytesIO(img_data))
            resized = tmp_img.resize((180, 120), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(resized)

            PreviewThumb.configure(image=img)
            PreviewThumb.image = img

            # Update title
            TitleBox.configure(state=NORMAL)
            TitleBox.delete(0, END)
            TitleBox.insert(END, video_info.get('title'))
            TitleBox.configure(state=DISABLED)

            # List formats
            formats = video_info.get('formats', [])
            audio_flag = checkAF.get()
            
            for f in formats:
                try:
                    # Get format details safely with fallbacks
                    format_id = f.get('format_id', 'N/A')
                    ext = f.get('ext', 'N/A')
                    vcodec = f.get('vcodec', '')
                    acodec = f.get('acodec', '')
                    
                    if audio_flag:
                        # Check if this is an audio-only format
                        if (vcodec == 'none' or not vcodec) and acodec != 'none':
                            abr = f.get('abr', 'N/A')
                            if isinstance(abr, (int, float)):
                                abr = f"{abr}k"
                            stream_item = (
                                f'format_id: {format_id} Codec: {acodec} '
                                f'BitRate: {abr} File Type: {ext}\n'
                            )
                            streamLB.insert(END, stream_item)
                    else:
                        # Video formats
                        if vcodec != 'none' and vcodec:
                            height = f.get('height', 'N/A')
                            fps = f.get('fps', 'N/A')
                            resolution = f"{height}p" if height != 'N/A' else 'N/A'
                            stream_item = (
                                f'format_id: {format_id} Resolution: {resolution} '
                                f'FPS: {fps} File Type: {ext}\n'
                            )
                            streamLB.insert(END, stream_item)
                except Exception as e:
                    print(f"Error processing format: {e}")
                    continue

        except Exception as e:
            showwarning("Window", f"WARNING: Unable to retrieve streams. Please check the URL. Error: {e}")
            return None

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
    Update the chosen variable with the format_id of the selected listbox item.
    """
    if streamLB.size() > 0:
        lb_item = streamLB.get(ANCHOR)
        arr = lb_item.split()
        format_id = arr[1]
        chosen.set(format_id)

def browse():
    """
    Open a dialog to select a directory and update the TextBox2 with the selected path.
    """
    download_path = filedialog.askdirectory()
    
    TextBox2.configure(state=NORMAL)
    TextBox2.delete(0, END)
    TextBox2.insert(END, download_path)
    TextBox2.configure(state=DISABLED)

def progress_hook(d):
    """
    Update progress bar during download.
    """
    if d['status'] == 'downloading':
        try:
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                ratio_complete = downloaded_bytes / total_bytes
                progress_bar['value'] = ratio_complete
                window.update_idletasks()
        except Exception:
            pass

def download():
    """
    Download the selected YouTube stream to the specified directory.
    """
    if streamLB.size() > 0 and chosen.get() != "0":
        output_path = TextBox2.get()
        format_id = chosen.get()
        
        # Configure options based on whether it's audio or video
        if checkAF.get():  # Audio Only
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:  # Video with audio
            ydl_opts = {
                # Format selection: chosen video format + best audio, fallback to best available
                'format': f'{format_id}+bestaudio[ext=m4a]/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
                # Ensure we merge the streams
                'merge_output_format': 'mp4',
                # Remove any video post-processing that might interfere with audio
                'postprocessors': [{
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                }],
                # Additional FFmpeg options for better audio handling
                'ffmpeg_args': ['-c:v', 'copy', '-c:a', 'aac'],
            }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url.get()])
            showinfo("Window", "Download Completed!")
        except Exception as e:
            showwarning("Window", f"WARNING: Download did not complete! Error: {e}")
            return None

def close():
    """
    Close the application window.
    """
    window.destroy()
    exit()

version = "1.2.5"
window = Tk()

# Window Title Bar Text
icon = ImageTk.PhotoImage(file=resource_path("./assets/003-download.png"))
window.iconphoto(False, icon)
WindowTitle = 'Youtube Downloader by Alykes - [' + version + ']'
window.title(string=WindowTitle)
window.configure(background="lightgrey")

# Set up tkinter variables
checkAF = IntVar()
PastaCheck = IntVar()
chosen = StringVar()  # Changed to StringVar since yt-dlp uses string format IDs
url = StringVar()

# Window Logo Placeholder
logo = ImageTk.PhotoImage(file=resource_path("./assets/hacker.gif"))
Label(window, image=logo, bg="lightgrey").grid(row=0, column=0, sticky=W)

# Default Thumbnail preview
thumb = Image.open(resource_path("./assets/mqdefault.jpg"))
thumb = thumb.resize((180, 120), Image.Resampling.LANCZOS)
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

# Window ListBox
streamLB = Listbox(window, width=88)
streamLB.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=W)

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

# Events
streamLB.bind("<ButtonRelease-1>", selection)
TextBox.bind("<ButtonRelease-1>", copy_pasta)

window.mainloop()
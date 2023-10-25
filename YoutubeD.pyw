import tkinter as tk
from pytube import YouTube
from tkinter import ttk
from tkinter import messagebox
import datetime
import requests
from PIL import Image, ImageTk
from io import BytesIO

def update_quality_combobox():
    url = url_entry.get()
    format_choice = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    yt = YouTube(url)

    if format_choice == "MP3":
        streams = yt.streams.filter(only_audio=True, file_extension='mp4')
        format_label = "abr"
        options = [f"{stream.abr} kbps (mp3)" for stream in streams if stream.abr]
    else:
        streams = yt.streams.filter(file_extension='mp4', progressive=True)
        format_label = "resolution"
        options = [f"{stream.resolution} ({stream.mime_type.split('/')[1]})" for stream in streams if stream.resolution]

    quality_combobox['values'] = options
    quality_combobox.set(options[0])

def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    selected_option = quality_combobox.get()

    if not url:
        messagebox.showerror("Error", "enter a Youtube URL.")
        return

    yt = YouTube(url)

    if format_choice == "MP3":
        streams = yt.streams.filter(only_audio=True, file_extension='mp4')
        format_label = "abr"
        options = [f"{stream.abr} kbps (mp3)" for stream in streams if stream.abr]
    else:
        streams = yt.streams.filter(file_extension='mp4', progressive=True)
        format_label = "resolution"
        options = [f"{stream.resolution} ({stream.mime_type.split('/')[1]})" for stream in streams if stream.resolution]

    try:
        index = [i for i, option in enumerate(options) if selected_option in option][0]
        stream = streams[index]
    except IndexError:
        messagebox.showerror("Error", "quality not found update options.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{yt.title}_{timestamp}.{format_choice.lower()}"

    try:
        stream.download(output_path='Downloads', filename=filename)
        messagebox.showinfo("Success", "Download success")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")

root = tk.Tk()
root.title("YouTube downloader by sloth")
root.geometry("360x200") 
root.resizable(False, False)

icon_url = "https://raw.githubusercontent.com/Pstrw/icon/main/Icon.png"
response = requests.get(icon_url)
icon_data = response.content
icon_image = Image.open(BytesIO(icon_data))
root.iconphoto(True, ImageTk.PhotoImage(icon_image))

format_label = ttk.Label(root, text="Choose a format:")
format_label.pack()

format_var = tk.StringVar()
mp3_radio = ttk.Radiobutton(root, text="MP3", variable=format_var, value="MP3")
mp3_radio.pack()
mp4_radio = ttk.Radiobutton(root, text="MP4", variable=format_var, value="MP4")
mp4_radio.pack()
format_var.set("MP3")

url_label = ttk.Label(root, text="Enter the YouTube URL:")
url_label.pack()

url_entry = ttk.Entry(root)
url_entry.pack()

quality_label = ttk.Label(root, text="Select Quality:")
quality_label.pack()

quality_var = tk.StringVar()
quality_combobox = ttk.Combobox(root, textvariable=quality_var, state="readonly")
quality_combobox.pack()

fetch_options_button = ttk.Button(root, text="Fetch Quality Options", command=update_quality_combobox)
fetch_options_button.pack()

download_button = ttk.Button(root, text="Download", command=download_video)
download_button.pack()

root.mainloop()

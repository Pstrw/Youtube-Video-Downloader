import tkinter as tk
from pytube import YouTube
from tkinter import ttk
from tkinter import messagebox
import datetime

def update_quality_combobox():
    url = url_entry.get()
    format_choice = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    yt = YouTube(url)

    if format_choice == "MP3":
        streams = yt.streams.filter(only_audio=True)
        format_label = "abr"
        options = [f"{stream.abr} kbps (mp3)" for stream in streams if stream.abr]
    else:
        streams = yt.streams.filter(file_extension='mp4')
        format_label = "resolution"
        options = [f"{stream.resolution} ({stream.mime_type.split('/')[1]})" for stream in streams if stream.resolution]

    quality_combobox['values'] = options
    quality_combobox.set(options[0])
    stream_dict = {option: stream for option, stream in zip(options, streams)}
    quality_combobox.stream_dict = stream_dict

def download_video():
    selected_option = quality_combobox.get()

    if not hasattr(quality_combobox, 'stream_dict'):
        messagebox.showerror("Error", "No quality options available. Fetch options first.")
        return

    if selected_option not in quality_combobox.stream_dict:
        messagebox.showerror("Error", "Quality not found. Update options.")
        return

    stream = quality_combobox.stream_dict[selected_option]
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{stream.title}_{timestamp}.{stream.subtype}"

    try:
        stream.download(output_path='Downloads', filename=filename)
        messagebox.showinfo("Success", "Download successful")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")

root = tk.Tk()
root.title("YouTube downloader by sloth")
root.geometry("360x200") 
root.resizable(False, False)

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

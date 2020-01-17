import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re
import pafy # https://github.com/mps-youtube/pafy
import os
from pprint import pprint
import threading

DESKTOP_FOLDER = os.path.join(os.path.expanduser('~'), 'Desktop') # Should work on Mac, Windows & Linux

class YoutubeDownloaderApp():
    def __init__(self, parent):
        # Create the window
        self.window = parent
        self.window.geometry("450x300")
        self.window.title("Youtube Downloader")
        self.video = True
        self.downloading = False

        self.question_label = tk.Label(self.window, text="Youtube URL of video to download")
        self.question_label.place(x=20, y=20)

        self.url_entry = tk.Entry(self.window)
        self.url_entry.place(x=20, y=60, w=300)
        self.url_entry.focus()

        self.question2_label = tk.Label(self.window, text="Save to folder")
        self.question2_label.place(x=20, y=100)

        self.target_folder_entry = tk.Entry(self.window)
        self.target_folder_entry.place(x=20,y=140, w=300)
        self.target_folder_entry.delete(0, tk.END)
        self.target_folder_entry.insert(tk.END, DESKTOP_FOLDER)
        self.pick_folder_button = tk.Button(self.window, text="Select folder", command=self.get_folder)
        self.pick_folder_button.place(x=350, y=140)

        self.get_video_button = tk.Button(self.window, text="Start download", command=self.start_download)
        self.get_video_button.place(x=200, y=190)
        self.mode_button = tk.Button(self.window, text="Switch to M4A (audio) mode", command=self.switch_mode)
        self.mode_button.place(x=20, y=190)
        self.close_button = tk.Button(self.window, text="Close", command=self.window.quit)
        self.close_button.place(x=350, y=190)

        self.progress=ttk.Progressbar(self.window,orient=tk.HORIZONTAL,length=100,mode='determinate')
        self.progress.place(x=20, y=230)
        self.info = tk.Label(self.window, text="")
        self.info.place(x=20,y=270)

    def switch_mode(self):
        self.video = not self.video
        if self.video:
            self.mode_button.configure(text="Switch to M4A (audio) mode")
        else:
            self.mode_button.configure(text="Switch to MP4 (video) mode")

    def start_download(self):
        url = self.url_entry.get()
        folder = self.target_folder_entry.get()
        if not self.downloading:
            threading.Thread(target=self.download_youtube).start()
    
    def get_folder(self):
        folder = filedialog.askdirectory(initialdir=DESKTOP_FOLDER, title = "Select folder to save to")
        self.target_folder_entry.delete(0, tk.END)
        self.target_folder_entry.insert(tk.END, folder)

    def _clean_file_name( self, original ):
        # Strip non-filename-friendly characters from the filename
        regex = re.compile('[^a-zA-Z0-9 \-.]')
        return regex.sub("", original )

    def download_youtube(self):
        self.downloading = True
        mode = "video" if self.video else "audio"
        url = self.url_entry.get()
        folder = self.target_folder_entry.get()
        video = pafy.new(url, ydl_opts={'nocheckcertificate': True, "--no-check-certificate": True})
        if mode == "video":
            best = video.getbestvideo(preftype="mp4")
        else:
            best = video.getbestaudio(preftype="m4a")
        saveAs = self._clean_file_name(video.title+"."+best.extension)
        saveAs = os.path.join(folder, saveAs)
        best.download(quiet=True, filepath=saveAs, callback=self.update_status)
        messagebox.showinfo("Done", f"Video \n{url}\n saved to\n{saveAs}")
        self.downloading = False
        return saveAs


    def update_status(self, stream, downloaded, ratio, rate, eta):
        percent = int(ratio*100)
        self.progress['value'] = percent
        mb = 1024*1024
        info_str = f"{downloaded//mb} of {stream//mb} MB downloaded. {int(eta)} seconds remaining."
        self.info.configure(text=info_str)
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()


# https://www.youtube.com/watch?v=Ug5IOh6PxWQ
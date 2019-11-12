import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re
import pafy # https://github.com/mps-youtube/pafy
import os
from pprint import pprint

class YoutubeDownloaderApp():
    def __init__(self, parent):
        # Create the window
        self.window = parent
        self.window.geometry("450x300")
        self.window.title("Youtube Downloader")

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
        self.target_folder_entry.insert(tk.END, os.getcwd())
        self.pick_folder_button = tk.Button(self.window, text="Select folder", command=self.get_folder)
        self.pick_folder_button.place(x=350, y=140)

        self.get_video_button = tk.Button(self.window, text="Download video", command=self.get_video)
        self.get_video_button.place(x=20, y=190)
        self.get_audio_button = tk.Button(self.window, text="Download audio", command=self.get_audio)
        self.get_audio_button.place(x=150, y=190)
        self.close_button = tk.Button(self.window, text="Close", command=self.window.quit)
        self.close_button.place(x=280, y=190)

        self.progress=ttk.Progressbar(self.window,orient=tk.HORIZONTAL,length=100,mode='determinate')
        self.progress.place(x=20, y=230)
        self.info = tk.Label(self.window, text="")
        self.info.place(x=20,y=270)

    def get_audio(self):
        url = self.url_entry.get()
        folder = self.target_folder_entry.get()
        saveas = self.download_youtube(url, folder=folder, video=False)
        messagebox.showinfo("Done", f"Video \n{url}\n saved to\n{saveas}")

    def get_video(self):
        url = self.url_entry.get()
        folder = self.target_folder_entry.get()
        saveas = self.download_youtube(url, folder=folder, video=True)
        messagebox.showinfo("Done", f"Video \n{url}\n saved to\n{saveas}")
    
    def get_folder(self):
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title = "Select folder to save to")
        self.target_folder_entry.delete(0, tk.END)
        self.target_folder_entry.insert(tk.END, folder)

    def _clean_file_name( self, original ):
        # Strip non-filename-friendly characters from the filename
        regex = re.compile('[^a-zA-Z0-9 \-.]')
        return regex.sub("", original )

    def download_youtube(self, url, folder, video=True):
        video = pafy.new(url, ydl_opts={'nocheckcertificate': True, "--no-check-certificate": True})
        if video:
            best = video.getbestvideo(preftype="mp4")
        else:
            best = video.getbestaudio(preftype="m4a")
        saveAs = self._clean_file_name(video.title+"."+best.extension)
        saveAs = os.path.join(folder, saveAs)
        best.download(quiet=True, filepath=saveAs, callback=self.update_status)
        return saveAs

# https://www.youtube.com/watch?v=Ug5IOh6PxWQ
    def update_status(self, stream, downloaded, ratio, rate, eta):
        #percent = int(ratio*100)
        #self.progress['value'] = percent
        #mb = 1024*1024
        #info_str = f"{downloaded//mb} of {stream//mb} MB downloaded. {eta} seconds remaining."
        #self.info.configure(text=info_str)
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()



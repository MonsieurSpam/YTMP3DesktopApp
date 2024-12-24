import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import time
from threading import Thread

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL Entry
        ttk.Label(main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Output Directory
        ttk.Label(main_frame, text="Save Location:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_path)
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Browse Button
        self.browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_location)
        self.browse_btn.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Convert", command=self.start_download)
        self.download_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Set default output directory to Downloads folder
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.output_path.set(default_path)

    def browse_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def download_audio(self):
        try:
            url = self.url_entry.get().strip()
            output_path = self.output_path.get()

            if not url:
                raise ValueError("Please enter a YouTube URL")

            if not output_path:
                raise ValueError("Please select an output location")

            # Set the output template for yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_var.set("Downloading...")
                info_dict = ydl.extract_info(url, download=True)

            # Get the actual downloaded file path from info_dict
            downloaded_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

            # Ensure the file exists
            if os.path.exists(downloaded_file):
                current_time = time.time()  # Get the current time in seconds

                # Set both the access time and modification time to the current time
                os.utime(downloaded_file, (current_time, current_time))

                self.status_var.set("Download completed!")
                messagebox.showinfo("Success", "Download completed successfully!")
            else:
                raise FileNotFoundError(f"Downloaded file not found: {downloaded_file}")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

        finally:
            self.progress.stop()
            self.download_btn.config(state='normal')
            self.url_entry.config(state='normal')


    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.status_var.set(f"Downloading... {d.get('_percent_str', '0%')}")
        elif d['status'] == 'finished':
            self.status_var.set("Converting to MP3...")

    def start_download(self):
        self.download_btn.config(state='disabled')
        self.url_entry.config(state='disabled')
        self.progress.start()
        Thread(target=self.download_audio, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

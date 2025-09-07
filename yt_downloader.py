import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import yt_dlp
import os
import re
import sys

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Download location
        ttk.Label(main_frame, text="Download Location:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser('~'), 'Downloads'))
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=50)
        path_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=2, column=2, padx=5)
        
        # Format selection (simplified to avoid FFmpeg requirement)
        ttk.Label(main_frame, text="Format:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="Best Available")
        format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, 
                                   values=["Best Available", "720p or lower", "480p or lower", "360p or lower"], width=20)
        format_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=4, column=0, pady=10)
        self.cancel_btn = ttk.Button(main_frame, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.grid(row=4, column=1, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to download")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Video info frame
        info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="5")
        info_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Info text area
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, width=80)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.info_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
    
    def validate_youtube_url(self, url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return re.match(youtube_regex, url) is not None
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percentage = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress_var.set(percentage)
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                percentage = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                self.progress_var.set(percentage)
            self.root.update_idletasks()
    
    def update_info_text(self, info):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if info:
            text = f"Title: {info.get('title', 'N/A')}\n"
            text += f"Channel: {info.get('uploader', 'N/A')}\n"
            text += f"Duration: {info.get('duration', 'N/A')} seconds\n"
            text += f"Views: {info.get('view_count', 'N/A'):,}\n"
            text += f"Upload Date: {info.get('upload_date', 'N/A')}\n"
            
            # Show available formats
            text += "\nAvailable Formats:\n"
            formats = info.get('formats', [])
            progressive_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') != 'none']
            
            for fmt in progressive_formats:
                if fmt.get('height'):
                    text += f"  {fmt['height']}p ({fmt['ext']})\n"
            
            self.info_text.insert(tk.END, text)
        
        self.info_text.config(state=tk.DISABLED)
    
    def get_video_info(self, url):
        """Get video information using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            return None
    
    def download_video(self):
        try:
            self.is_downloading = True
            url = self.url_var.get()
            path = self.path_var.get()
            format_choice = self.format_var.get()
            
            # Configure download options - only use progressive formats (no FFmpeg required)
            download_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'quiet': True,
                'progress_hooks': [self.progress_hook],
                # Only download formats that don't require merging
                'format': 'best[height<=720][vcodec!=av01]',  # Default to best quality up to 720p
            }
            
            # Adjust format based on user selection
            if format_choice == "720p or lower":
                download_opts['format'] = 'best[height<=720][vcodec!=av01]'
            elif format_choice == "480p or lower":
                download_opts['format'] = 'best[height<=480][vcodec!=av01]'
            elif format_choice == "360p or lower":
                download_opts['format'] = 'best[height<=360][vcodec!=av01]'
            
            # Download the video
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([url])
            
            self.status_var.set("Download Complete!")
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.progress_var.set(0)
    
    def start_download(self):
        url = self.url_var.get().strip()
        path = self.path_var.get()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not self.validate_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
            
        if not path:
            messagebox.showerror("Error", "Please select a download location")
            return
            
        if not os.path.exists(path):
            messagebox.showerror("Error", "The selected directory does not exist")
            return
        
        # Get video info first
        info = self.get_video_info(url)
        if info:
            self.update_info_text(info)
        else:
            messagebox.showerror("Error", "Could not get video information")
            return
        
        self.status_var.set("Downloading...")
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        # Start download in a separate thread
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()
    
    def cancel_download(self):
        if self.is_downloading:
            self.status_var.set("Cancelling...")
            self.is_downloading = False

if __name__ == "__main__":
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("Installing yt-dlp...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        import yt_dlp
    
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

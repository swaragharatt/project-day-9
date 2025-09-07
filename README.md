project-day-9
## YouTube Video Downloader

A **Python GUI application** that allows users to download YouTube videos in multiple resolutions without requiring FFmpeg.
This project helps users save YouTube videos directly to their system with a simple and beginner-friendly interface.

---

## Features

Download YouTube videos in various resolutions (Best Available, 720p, 480p, 360p)

Fetch and display video information: title, channel, duration, views, upload date

Real-time download progress with a progress bar

GUI folder picker for download location

Cancel ongoing downloads anytime

Works on Windows, Mac, and Linux

Beginner-friendly and lightweight

---

## Technologies Used

Python 3 – Core programming language

tkinter – GUI interface

yt-dlp – YouTube video extraction and download

threading – Non-blocking download execution

os, re, sys – File handling and URL validation

---

## Project Structure

youtube-downloader/
│── youtube_downloader.py # Main Python script
│── README.md # Documentation

---

#How to Run

Clone the repository.

Install dependencies (yt-dlp will auto-install if not present):

pip install yt-dlp

Run the script:

python youtube_downloader.py

Enter the YouTube URL, choose download location and format, then click Download.

Files will be saved automatically in the chosen folder.

Example Downloads Folder:

Downloads/
   ├── Video_Title.mp4
   ├── Another_Video.mp4
   └── Sample_Video.mp4

---

## Output 

<img width="867" height="654" alt="Screenshot 2025-09-07 163912" src="https://github.com/user-attachments/assets/ce7ba60a-1816-489d-b8f1-5b5523c7bb02" />


Author
Swara Gharat

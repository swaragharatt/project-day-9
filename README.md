# project-day-9
This project provides an easy-to-use interface to fetch video information and download videos directly to your system.

Features

Download YouTube videos in various resolutions (Best, 720p, 480p, 360p)

Fetch and display video information: title, channel, duration, views, upload date

Real-time download progress with progress bar

GUI folder picker for download location

Cancel ongoing downloads at any time

Beginner-friendly and lightweight

Technologies Used

Python 3 – Core programming language

tkinter – GUI interface

yt-dlp – YouTube video extraction and download

threading – Non-blocking download execution

os, re, sys – File handling and URL validation

Project Structure

youtube-downloader/
│── youtube_downloader.py # Main Python script
│── README.md # Documentation

How to Run

Clone the repository.

Install dependencies (yt-dlp will auto-install if not present):

pip install yt-dlp


Run the script:

python youtube_downloader.py


Enter the YouTube URL, choose download location and format, then click Download.

Example Output Structure

Downloads/
├── Video_Title.mp4
├── Another_Video.mp4

## Output 

<img width="867" height="654" alt="Screenshot 2025-09-07 163912" src="https://github.com/user-attachments/assets/d0d7c65d-6173-42b1-9e02-d28354a1482d" />


Author

Swara Gharat

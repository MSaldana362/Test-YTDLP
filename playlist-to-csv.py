import csv
import sys
import yt_dlp
import pyinputplus as pyip

def extract_playlist_info(playlist_url, output_file="playlist_info.csv"):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Extract metadata without downloading
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_data = ydl.extract_info(playlist_url, download=False)
        except yt_dlp.utils.DownloadError as e:
            print(f"Error: {e}")
            sys.exit(1)

    if 'entries' not in playlist_data:
        print("Failed to retrieve playlist data.")
        sys.exit(1)

    videos = playlist_data['entries']
    
    # Writing the data to a CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Channel", "URL"])  # Header

        for video in videos:
            title = video.get('title', 'Unknown')
            channel = video.get('uploader', 'Unknown')
            url = f"https://www.youtube.com/watch?v={video['id']}"
            writer.writerow([title, channel, url])

    print(f"Playlist data saved to '{output_file}'.")

if __name__ == "__main__":
    url = pyip.inputURL("Enter YouTube playlist URL: ")
    output = pyip.inputStr("Enter output CSV filename (default: playlist_info.csv): ", blank=True)
    output_file = output if output else "playlist_info.csv"
    extract_playlist_info(url, output_file)

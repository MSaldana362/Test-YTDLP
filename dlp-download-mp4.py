import yt_dlp

def download_video(url):
    # Set options for download
    opt = {
        'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(opt) as ydl:
        # Extract video information without downloading it first
        info_dict = ydl.extract_info(url, download=False)
        # Get the title from the information dictionary
        video_title = info_dict.get('title', 'Unknown Title')
        print(f"Title of the video: {video_title}")

        # Download
        ydl.download(url)

if __name__ == "__main__":
    video_url = input("Enter video url: ")
    download_video(video_url)
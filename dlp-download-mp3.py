import os
import yt_dlp
import eyed3
import pyinputplus as pyip
from pathlib import Path


def get_album_info():
    print("Getting download info...")

    info = {
        'artist': None,     # Album artist
        'album': None,      # Album title
        'year': None,       # Album year
        'tracks': None,     # Track names
        'dir': None,        # Album folder
        'url': None         # YouTube URL for album
    }

    info_artist = pyip.inputStr(prompt="Enter artist name: ")
    info_album = pyip.inputStr(prompt="Enter album name: ")
    info_year = pyip.inputNum(prompt="Enter album year: ", min=1000, max=9999)

    info_url = pyip.inputURL(prompt="Enter YouTube URL: ")

    info_dir = f'{info_artist} - {info_album} ({info_year})'

    info['artist'] = info_artist
    info['album'] = info_album
    info['year'] = info_year

    info['dir'] = info_dir
    info['url'] = info_url

    info['tracks'] = get_playlist_tracks(info_url)

    return info


def download_playlist_as_mp3(url, folder):
    print("Downloading YouTube playlist as MP3...")

    # Set download options
    ydl_opt = {
        'format': 'bestaudio/best',
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False
    }

    # Download
    with yt_dlp.YoutubeDL(ydl_opt)as ydl:
        ydl.download([url])


def get_playlist_tracks(url):
    print("Getting YouTube playlist track info...")

    # Set options
    ydl_opts = {
        'extract_flat': True,
        'playlistend': None
    }

    # Get playlist info
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(url, download=False)

    # Extract titles from playlist info
    titles = [entry['title'] for entry in playlist_info['entries']]

    # Display track info
    print("Tracks".center(40,"-"))
    for index, item in enumerate(titles):
        print(f"{index+1:02d}".ljust(5) + f"{item}")

    return titles


def create_album_info_txt(info):
    print("Creating TXT with album info...")

    folder = info['dir']
    url = info['url']
    tracks = info['tracks']

    file_name = Path(folder) / Path('info.txt')
    info_file = open(file_name, 'w')

    info_file.write(f'{folder}\n')
    info_file.write(f'\n{url}\n')

    info_file.write('\n' + 'Tracks'.center(20, '-') + '\n')

    for index, item in enumerate(tracks):
        info_file.write(f"{index+1:02d}".ljust(5) + f"{item}" + "\n")

    info_file.close()


def set_track_tags(info):
    print("Setting tags...")

    # Get album info
    artist = info['artist']
    album = info['album']
    year = info['year']
    tracks = info['tracks']
    folder = info['dir']

    # Loop through all tracks
    for index, item in enumerate(tracks):
        track_number = index + 1
        track_title = item

        # Create assumed path for track
        track_path = Path.cwd() / Path(folder) / Path(f'{track_title}.mp3')

        # Set tags if file exists
        if os.path.exists(track_path):
            audio_file = eyed3.load(track_path)

            audio_file.tag.title = track_title
            audio_file.tag.artist = artist
            audio_file.tag.album = album
            audio_file.tag.recording_date = eyed3.core.Date(year)
            audio_file.tag.track_num = track_number

            audio_file.tag.save()
        else:
            print(f"Track {track_title} does not exist!")


if __name__ == "__main__":
    print("Hello World!")

    # Get album info
    album_info = get_album_info()

    # Create directory
    os.mkdir(album_info['dir'])

    # Create a TXT file with album info inside directory
    create_album_info_txt(album_info)

    # Download
    download_playlist_as_mp3(album_info['url'],album_info['dir'])

    # Add tags to all tracks
    set_track_tags(album_info)





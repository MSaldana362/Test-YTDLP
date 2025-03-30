"""
Convert to MP3
"""

import os
from typing import List, Dict
from pathlib import Path
import pyinputplus as pyip
import yt_dlp
import eyed3


def get_track_info(url: str) -> str | List[str]:

    ydl_options = {"extract_flat": True, "playlistend": None}

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            return f"Error: {e}"

        if not info:
            return "Error: Could not extract info."

        if "entries" in info:
            print("Playlist Tracks".center(40, "-"))
            titles = [entry["title"] for entry in info["entries"]]
            for index, item in enumerate(titles):
                print(f"{index+1:02d}".ljust(5) + f"{item}")

            return titles

        print("Single Track".center(40, "-"))
        title = info["title"]
        print(f"{title}")

        return [title]


def get_music_info() -> Dict[str, str | List[str]]:

    info_artist = pyip.inputStr(prompt="Enter artist name: ")
    info_album = pyip.inputStr(prompt="Enter album name: ")
    info_year = pyip.inputNum(prompt="Enter album year: ", min=1000, max=9999)
    info_url = pyip.inputURL(prompt="Enter YouTube URL: ")

    info_tracks = get_track_info(info_url)
    info_dir = f"{info_artist} - {info_album} ({info_year})"

    info: dict[str, str | List[str]] = {
        "artist": info_artist,  # Album artist
        "album": info_album,  # Album title
        "year": info_year,  # Album year
        "tracks": info_tracks,  # Track names
        "dir": info_dir,  # Album folder
        "url": info_url,  # YouTube URL for album
    }
    return info


def create_info_txt(info):
    folder = info["dir"]
    url = info["url"]
    tracks = info["tracks"]

    file_name = Path(folder) / Path("info.txt")
    info_file = open(file_name, "w")

    info_file.write(f"{folder}\n")
    info_file.write(f"\n{url}\n")

    info_file.write("\n" + "Tracks".center(20, "-") + "\n")

    for index, item in enumerate(tracks):
        info_file.write(f"{index+1:02d}".ljust(5) + f"{item}" + "\n")

    info_file.close()


def download_as_mp3(url, folder):
    ydl_opt = {
        "format": "bestaudio/best",
        "outtmpl": f"{folder}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "noplaylist": False,
    }

    with yt_dlp.YoutubeDL(ydl_opt) as ydl:
        ydl.download([url])


def set_track_tags(info):
    print("Applying tags...")

    # Get album info
    artist = info["artist"]
    album = info["album"]
    year = info["year"]
    tracks = info["tracks"]
    folder = info["dir"]

    # Loop through all tracks
    for index, item in enumerate(tracks):
        track_number = index + 1
        track_title = item

        # Create assumed path for track
        track_path = Path.cwd() / Path(folder) / Path(f"{track_title}.mp3")

        # Set tags if file exists
        if os.path.exists(track_path):
            audio_file = eyed3.load(track_path)

            if audio_file:

                audio_file.tag.title = track_title
                audio_file.tag.artist = artist
                audio_file.tag.album = album
                audio_file.tag.recording_date = eyed3.core.Date(year)
                audio_file.tag.track_num = track_number

                audio_file.tag.save()
        else:
            print(f"Track {track_title} does not exist!")


if __name__ == "__main__":
    print("YouTube Music Downloader".center(80, "-"))

    music_info = get_music_info()

    os.mkdir(str(music_info["dir"]))

    create_info_txt(music_info)

    download_as_mp3(music_info["url"], music_info["dir"])

    set_track_tags(music_info)

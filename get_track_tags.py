"""
Get tags from an MP3 file.
"""

import os
from typing import TypedDict
import pyinputplus as pyip  # type: ignore
import eyed3  # type: ignore


class TrackInfo(TypedDict):
    """Type for track info."""

    title: str
    artist: str
    album: str
    year: int
    track_number: int


def get_track_path() -> str:
    """Get path for MP3 file.

    Returns:
        str: MP3 file path
    """
    input_path = pyip.inputStr(prompt="Enter MP3 file path: ", blank=False)
    return input_path


def get_track_info(track_path: str) -> TrackInfo | None:
    """Extract tags from an audio file.

    Args:
        track_path (str): Path to MP3 file to extract tags from.

    Returns:
        TrackInfo | None: Dictionary containing track info.
    """

    if not os.path.exists(track_path):
        return None

    audio_file = eyed3.load(track_path)
    if not audio_file:
        return None

    audio_track_info: TrackInfo = {
        "title": audio_file.tag.title,
        "artist": audio_file.tag.artist,
        "album": audio_file.tag.album,
        "year": int(str(audio_file.tag.recording_date)),
        "track_number": audio_file.tag.track_num[0],
    }
    return audio_track_info


if __name__ == "__main__":

    file_path: str = get_track_path()
    file_info = get_track_info(file_path)

    if not file_info:
        print("No Track Info")
    else:
        print("Track Info".center(40, "-"))
        for key, value in file_info.items():
            print(f"{key.title()}".ljust(20) + f"{value}")

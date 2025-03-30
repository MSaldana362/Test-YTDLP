"""
Transfer MP3 files from one directory to another in track order.
"""

from typing import List, TypedDict
from pathlib import Path
import shutil
import pyinputplus as pyip  # type: ignore
import eyed3  # type: ignore


class TrackInfo(TypedDict):
    """Type for track info."""

    title: str
    artist: str
    album: str
    year: int
    track_number: int


def input_directory(prompt: str) -> Path:
    """Get path to a directory.

    Args:
        prompt (str): Prompt when asking for user input.

    Returns:
        Path: Path to directory.
    """

    while True:
        input_path = Path(pyip.inputFilepath(prompt, blank=False))
        if input_path.is_dir():
            return input_path

        print("Invalid directory. Please enter a valid directory path.")


def get_directory_files(directory: Path) -> List[Path]:
    """Get all files in a directory.

    Args:
        directory (Path): Directory.

    Returns:
        List[Path]: List of files in directory.
    """

    files: List[Path] = []

    for file in directory.iterdir():
        if file.is_file():
            files.append(file.resolve())

    return files


def get_mp3_tags(mp3_file: Path) -> TrackInfo | None:
    """Get tags of an MP3 file. This includes:
    - Title
    - Artist
    - Album
    - Year
    - Track Number

    Args:
        mp3_file (Path): Path to MP3 file.

    Returns:
        TrackInfo | None: MP3 tags. Returns `None` if unsuccessful.
    """

    audio_file = eyed3.load(mp3_file)
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


def sort_mp3_tags(mp3_file: Path) -> str | int:
    """Custom sorting function to sort MP3 files according to their track numbers.
    - If an MP3 file does not have a track number, the track title is used instead.
    - If an MP3 file does not have a track title, the file name is used instead.

    Args:
        mp3_file (Path): Path to MP3 file.

    Returns:
        str: Item to be used for sorting.
    """

    track_info = get_mp3_tags(mp3_file)
    if not track_info:
        return mp3_file.name

    track_number = track_info.get("track_number")
    if track_number:
        return track_number

    track_title = track_info.get("title")
    if track_title:
        return track_title

    return mp3_file.name


def get_sorted_mp3_files(files: List[Path]) -> list[Path] | None:
    """From a list of files in a directory, return a list of sorted MP3 files.

    Args:
        files (List[Path]): List of files in a directory.

    Returns:
        list[Path] | None: List of sorted MP3 files in a directory.
    """

    mp3_files: List[Path] = []
    desired_suffix = ".mp3"

    for file in files:
        if file.suffix == desired_suffix:
            mp3_files.append(file)

    if len(mp3_files) == 0:
        print("No MP3 files found in this directory.")
        return None

    print("Before:")
    for file in mp3_files:
        print(f"\t{file.name}")

    mp3_files.sort(key=sort_mp3_tags)

    print("After:")
    for file in mp3_files:
        print(f"\t{file.name}")

    return mp3_files


if __name__ == "__main__":

    source_directory = input_directory("Enter album directory path: ")
    target_directory = input_directory(
        "Enter target directory. This is where the album directory will be copied: "
    )

    print(f"\tSource directory: {source_directory}")
    print(f"\tTarget directory: {target_directory}")

    directory_files = get_directory_files(source_directory)

    sorted_mp3_files = get_sorted_mp3_files(directory_files)
    if sorted_mp3_files:

        new_directory = target_directory / source_directory.name
        if not new_directory.exists():
            print(f"Creating directory at '{new_directory}'")
            Path.mkdir(new_directory)

        for file in sorted_mp3_files:
            print(f"Copying file '{file.name}'")
            target_path = new_directory / file.name
            shutil.copy2(file, target_path)

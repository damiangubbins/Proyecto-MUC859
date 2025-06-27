import argparse

from pyautogui import FailSafeException

from console import clear
from player import Player

parser = argparse.ArgumentParser(
    prog="GIMidi Player v0.1.0", description="Play a song from a given path."
)
parser.add_argument("song_path", type=str, help="Path to the song file to be played.")

if __name__ == "__main__":
    args = parser.parse_args()
    SONG_PATH = args.song_path
    player = Player(SONG_PATH)
    try:
        player.play()
    except KeyboardInterrupt:
        clear()
    except FailSafeException:
        clear()
    finally:
        clear()

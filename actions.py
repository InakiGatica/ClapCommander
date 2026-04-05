import subprocess
import os
import sys
import pygame

# Application paths
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
DISCORD_PATH = r"C:\Users\Iña\AppData\Local\Discord\Update.exe"
MUSIC_PATH = os.path.join(BASE_DIR, "ironman.mp3")

# State
_music_started = False


def open_brave():
    """Open Brave browser with YouTube."""
    try:
        subprocess.Popen([BRAVE_PATH, "https://www.youtube.com"])
        print("Brave opened with YouTube!")
    except FileNotFoundError:
        print(f"Error: Brave not found at {BRAVE_PATH}")
        print("Please update BRAVE_PATH in actions.py with the correct path.")


def open_discord():
    """Open Discord."""
    try:
        subprocess.Popen([DISCORD_PATH, "--processStart", "Discord.exe"])
        print("Discord opened!")
    except FileNotFoundError:
        print(f"Error: Discord not found at {DISCORD_PATH}")
        print("Please update DISCORD_PATH in actions.py with the correct path.")


def init_audio():
    pygame.mixer.init()


def play_music():
    try:
        if not os.path.exists(MUSIC_PATH):
            print(f"Error: Music file not found at {MUSIC_PATH}")
            return
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play()
        print("Playing ironman.mp3!")
    except Exception as e:
        print(f"Error playing music: {e}")


def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def iron_man_sequence():
    """Open Brave, Discord, and play ironman.mp3. Stop music if already playing."""
    global _music_started

    if not _music_started:
        open_brave()
        open_discord()
        play_music()
        _music_started = True
    else:
        stop_music()
        _music_started = False

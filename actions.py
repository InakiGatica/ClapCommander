import subprocess
import os
import sys
import pygame
import ctypes
import settings
import pyautogui

# Application paths
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# State
_music_started = False


def open_apps():
    """Open apps from settings list. First app gets the URL."""
    apps = settings.get("apps", [])
    url = settings.get("double_clap_url", "https://www.youtube.com")
    for i, app_path in enumerate(apps):
        try:
            if i == 0:  # first app gets the URL
                subprocess.Popen([app_path, url])
                print(f"Opened: {app_path} with {url}")
            else:
                subprocess.Popen([app_path])
                print(f"Opened: {app_path}")
        except FileNotFoundError:
            print(f"Error: App not found at {app_path}")


def init_audio():
    pygame.mixer.init()


def play_music():
    try:
        music_path = settings.get("music_path", os.path.join(BASE_DIR, "ironman.mp3"))
        if not os.path.exists(music_path):
            print(f"Error: Music file not found at {music_path}")
            return
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        print(f"Playing {music_path}!")
    except Exception as e:
        print(f"Error playing music: {e}")


def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def iron_man_sequence():
    """Open apps and play ironman.mp3. Stop music if already playing."""
    global _music_started

    if not _music_started:
        open_apps()
        play_music()
        _music_started = True
    else:
        stop_music()
        _music_started = False


def lock_pc():
    """Lock the PC."""
    ctypes.windll.user32.LockWorkStation()
    print("PC locked!")


def mute_toggle():
    """Mute/Unmute system audio using pyautogui."""
    try:
        pyautogui.press('volumemute')
        print("Mute toggled!")
    except Exception as e:
        print(f"Error toggling mute: {e}")
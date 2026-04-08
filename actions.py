import subprocess
import os
import sys
import pygame
import ctypes
import settings
import pyautogui
import random
from win11toast import notify
from tray import update_tray_song

# Application paths
if getattr(sys, 'frozen', False):
    # Running as .exe - music folder next to the exe
    EXE_DIR = os.path.dirname(sys.executable)
else:
    # Running as .py - music folder next to the script
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = getattr(sys, '_MEIPASS', EXE_DIR)
MUSIC_FOLDER = os.path.join(EXE_DIR, "music")
ICON_PATH = os.path.join(BASE_DIR, "icon.ico")
PNG_PATH = os.path.join(BASE_DIR, "icon.png")

# State
_music_started = False
_listener_ref = None


def set_listener(listener):
    """Registrar el listener para controlar recalibración."""
    global _listener_ref
    _listener_ref = listener


def get_random_music() -> str or None:
    """Get a random music file from the music folder."""
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER, exist_ok=True)
        return None
    
    files = [f for f in os.listdir(MUSIC_FOLDER) 
             if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
    
    if not files:
        return None
    
    return os.path.join(MUSIC_FOLDER, random.choice(files))


def show_notification(title: str, message: str):
    try:
        icon_url = "file:///" + PNG_PATH.replace("\\", "/")
        notify(
            title=title,
            body=message,
            icon={"src": icon_url, "placement": "appLogoOverride"},
            app_id="ClapCommander"
        )
    except Exception as e:
        print(f"Notification error: {e}")


def open_apps():
    apps = settings.get("apps", [])
    url = settings.get("double_clap_url", "https://www.youtube.com")
    
    for i, app_entry in enumerate(apps):
        if not app_entry.strip():
            continue
        try:
            # Check if it's a .exe path or a shell command
            if os.path.isabs(app_entry) or app_entry.endswith('.exe'):
                # It's a file path
                if i == 0 and url:
                    subprocess.Popen([app_entry, url])
                else:
                    subprocess.Popen([app_entry])
            else:
                # It's a shell command - run through PowerShell for full PATH access
                subprocess.Popen(
                    ['powershell', '-WindowStyle', 'Normal', '-Command', app_entry],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            print(f"Opened: {app_entry}")
        except Exception as e:
            print(f"Error opening {app_entry}: {e}")


def init_audio():
    pygame.mixer.init()


def play_music():
    try:
        music_path = get_random_music()
        if not music_path:
            print("No music files found in music folder.")
            return
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        print(f"Playing: {os.path.basename(music_path)}")
        update_tray_song(os.path.basename(music_path))
        if _listener_ref:
            _listener_ref.set_music_playing(True)
    except Exception as e:
        print(f"Error playing music: {e}")


def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        update_tray_song(None)
        if _listener_ref:
            _listener_ref.set_music_playing(False)


def iron_man_sequence():
    """Open apps and play random music from music folder. Stop music if already playing."""
    global _music_started

    if not _music_started:
        open_apps()
        play_music()
        show_notification(
            "ClapCommander ⚡",
            f"Secuencia activada — {len(settings.get('apps', []))} apps abiertas"
        )
        _music_started = True
    else:
        stop_music()
        show_notification("ClapCommander ⚡", "Música detenida")
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
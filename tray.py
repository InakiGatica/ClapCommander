import pystray
from PIL import Image
import sys
import os

_tray_icon = None

def create_icon():
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(BASE_DIR, "icon.ico")
    return Image.open(icon_path)

def update_tray_song(song_name: str):
    """Update tray tooltip and menu with current song."""
    global _tray_icon
    if _tray_icon is None:
        return
    label = f"♪ {song_name}" if song_name else "♪ Sin música"
    _tray_icon.title = f"ClapCommander — {label}"
    # Rebuild menu with song info
    _rebuild_menu(label)

def _rebuild_menu(song_label: str):
    global _tray_icon
    if _tray_icon is None:
        return
    items = [pystray.MenuItem(song_label, None, enabled=False)]
    if _tray_icon._on_settings:
        items.append(pystray.MenuItem("Settings", _tray_icon._on_settings))
    items.append(pystray.MenuItem("Quit", _tray_icon._on_quit))
    _tray_icon.menu = pystray.Menu(*items)

def create_tray(on_quit, on_settings=None):
    global _tray_icon
    song_label = "♪ Sin música"
    menu_items = [pystray.MenuItem(song_label, None, enabled=False)]
    if on_settings:
        menu_items.append(pystray.MenuItem("Settings", on_settings))
    menu_items.append(pystray.MenuItem("Quit", on_quit))
    icon = pystray.Icon(
        "clapcommander",
        create_icon(),
        "ClapCommander",
        menu=pystray.Menu(*menu_items)
    )
    icon._on_quit = on_quit
    icon._on_settings = on_settings
    _tray_icon = icon
    return icon
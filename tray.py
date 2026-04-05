import pystray
from PIL import Image
import sys
import os


def create_icon():
    """Load icon.ico from the app directory."""
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(BASE_DIR, "icon.ico")
    return Image.open(icon_path)


def create_tray(on_quit, on_settings=None):
    """Create system tray icon with menu."""
    menu_items = []
    if on_settings:
        menu_items.append(pystray.MenuItem("Settings", on_settings))
    menu_items.append(pystray.MenuItem("Quit", on_quit))

    icon = pystray.Icon(
        "clapcommander",
        create_icon(),
        "ClapCommander",
        menu=tuple(menu_items)
    )
    return icon

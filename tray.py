import pystray
from PIL import Image, ImageDraw


def create_icon():
    """Draw a simple green circle on black 64x64 image."""
    image = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill="green", outline="darkgreen", width=2)
    return image


def create_tray(on_quit):
    """Create system tray icon with menu."""
    icon = pystray.Icon(
        "clap_detector",
        create_icon(),
        "Clap Detector",
        menu=(
            pystray.MenuItem("Quit", on_quit),
        )
    )
    return icon

# Iron Man Mode - Clap Detector

A Windows desktop application that detects double claps to trigger an "Iron Man" sequence — opening Brave browser with YouTube, Discord, and playing the Iron Man theme song.

## Features

- **Double clap detection** using audio energy analysis
- **First double clap**: Opens Brave with YouTube, launches Discord, plays ironman.mp3
- **Second double clap**: Stops music and closes the detector
- **System tray integration** with Quit option
- **Auto-calibration** — measures ambient noise and sets threshold automatically
- **Compiled executable** — runs as a single .exe file

## Requirements

- Python 3.12+
- sounddevice
- numpy
- pygame
- pystray
- Pillow

Or use the pre-compiled `dist/main.exe` — no Python needed!

## Installation

### From Source

```bash
pip install sounddevice numpy pygame pystray pillow
```

### Pre-compiled

Just run `dist/main.exe` — no installation needed!

## Usage

1. Run the application
2. Stay quiet for 3 seconds during auto-calibration
3. **Double clap** to trigger the Iron Man sequence:
   - Opens Brave browser → youtube.com
   - Launches Discord
   - Plays ironman.mp3
4. **Double clap again** to stop music and close the detector
5. Alternatively, use the system tray icon → Quit

## Autostart (optional)

To run on Windows startup:

1. Create a shortcut to `main.exe`
2. Press `Win + R`, type `shell:startup`
3. Place the shortcut in the startup folder

Or use Task Scheduler to run the .exe on login.

## Project Structure

```
IronManClaps/
├── config.py          # Constants (sample rate, thresholds, device)
├── detector.py        # ClapDetector class (double clap logic)
├── listener.py       # AudioListener with sounddevice
├── actions.py        # open_brave, open_discord, play_music, iron_man_sequence
├── tray.py           # System tray icon with pystray
├── main.py           # Entry point, ties everything together
├── ironman.mp3       # Theme song (your own file!)
└── dist/
    └── main.exe      # Compiled executable
```

## Calibration

The app auto-calibrates on startup by measuring 3 seconds of ambient noise and setting the energy threshold to 15x the RMS. If it's too sensitive or not sensitive enough, adjust `ENERGY_THRESHOLD` in `config.py`.

## Known Issues

- If using a different microphone, update `DEVICE_INDEX` in `config.py`
- Discord path may vary — update `DISCORD_PATH` in `actions.py` if needed

## License

MIT — do whatever you want with it!
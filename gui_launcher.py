from gui import ConfigWindow

# Standalone launcher for the settings window
# Used when opening Settings from the system tray (runs in separate process)

if __name__ == "__main__":
    window = ConfigWindow()
    window.show()
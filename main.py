import os
import signal
import threading
import time
import warnings
from listener import AudioListener, calibrate
import actions
from tray import create_tray

warnings.filterwarnings("ignore")


def main():
    """Main entry point for clap detector."""
    actions.init_audio()

    threshold = calibrate()

    def trigger_and_exit():
        actions.iron_man_sequence()
        if not actions._music_started:  # second clap - music was stopped, exit detector
            listener.stop()
            tray_icon.stop()
            os.kill(os.getpid(), signal.SIGTERM)

    listener = AudioListener(
        on_double_clap=trigger_and_exit,
        threshold=threshold
    )

    def on_quit():
        actions.stop_music()
        listener.stop()
        tray_icon.stop()
        os.kill(os.getpid(), signal.SIGTERM)

    tray_icon = create_tray(on_quit=on_quit)

    threading.Thread(target=tray_icon.run, daemon=True).start()

    print("Clap detector started. Double clap to trigger Iron Man sequence.")
    print("Press Ctrl+C to stop.")

    try:
        listener.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        on_quit()


if __name__ == "__main__":
    main()

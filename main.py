import os
import signal
import threading
import time
import warnings
from listener import AudioListener, calibrate
import actions
import settings
from tray import create_tray
from gui import ConfigWindow, is_first_run

warnings.filterwarnings("ignore")


def main():
    """Main entry point for clap detector."""
    # First run: show config window
    if is_first_run():
        config_window = ConfigWindow()
        config_window.show()

    actions.init_audio()

    threshold = calibrate()

    # Determine triple clap action from settings
    triple_action_name = settings.get("triple_clap_action", "Lock PC")
    if triple_action_name == "Lock PC":
        triple_action = actions.lock_pc
    elif triple_action_name == "Mute/Unmute":
        triple_action = actions.mute_toggle
    else:
        triple_action = None

    def trigger_and_exit():
        actions.iron_man_sequence()
        if not actions._music_started:  # music was stopped, check second action
            second_action = settings.get("second_double_clap_action", "Stop music + close detector")
            if second_action == "Stop music + close detector":
                listener.stop()
                tray_icon.stop()
                os.kill(os.getpid(), signal.SIGTERM)

    # Event to signal settings window request from tray
    settings_requested = threading.Event()

    def on_settings():
        settings_requested.set()

    listener = AudioListener(
        on_double_clap=trigger_and_exit,
        on_triple_clap=triple_action,
        threshold=threshold,
        verbose=True
    )

    actions.set_listener(listener)

    def on_quit():
        actions.stop_music()
        listener.stop()
        tray_icon.stop()
        os.kill(os.getpid(), signal.SIGTERM)

    tray_icon = create_tray(on_quit=on_quit, on_settings=on_settings)

    threading.Thread(target=tray_icon.run, daemon=True).start()

    print("ClapCommander started. Double clap to trigger Iron Man sequence.")
    print("Press Ctrl+C to stop.")

    try:
        listener.start()
        while True:
            time.sleep(0.1)
            # Check if settings was requested from tray
            if settings_requested.is_set():
                settings_requested.clear()
                config_window = ConfigWindow()
                config_window.show()
    except KeyboardInterrupt:
        on_quit()


if __name__ == "__main__":
    main()
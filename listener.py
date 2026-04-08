import sounddevice as sd
import numpy as np
import time as time_module
import config
import threading
from gesture_engine import GestureEngine


def calibrate():
    """Auto-calibrate the energy threshold by measuring ambient noise."""
    print("Calibrating... keep quiet for 3 seconds")

    recording = sd.rec(
        int(config.CALIBRATION_SECONDS * config.SAMPLE_RATE),
        samplerate=config.SAMPLE_RATE,
        channels=1,
        device=config.DEVICE_INDEX
    )
    sd.wait()  # block until recording finishes

    rms = np.sqrt(np.mean(recording ** 2))
    threshold = rms * 8  # safe margin

    print(f"Calibration done. Threshold set to: {threshold:.4f}")
    return threshold


class AudioListener:
    """Listens for audio input and detects claps."""

    def __init__(self, on_double_clap=None, on_triple_clap=None, verbose=False, threshold=None):
        self.verbose = verbose
        self.detector = GestureEngine(
            on_double_clap=on_double_clap,
            on_triple_clap=on_triple_clap
        )
        self.stream = None
        self.threshold = threshold if threshold is not None else config.ENERGY_THRESHOLD
        self.prev_energy = 0.0
        self._recalibrate_interval = 300  # segundos
        self._recalibrate_timer = None
        self._is_music_playing = False

    def set_music_playing(self, playing: bool):
        """Llamar desde actions.py cuando inicia/detiene música."""
        self._is_music_playing = playing

    def _schedule_recalibration(self):
        """Programa la próxima recalibración."""
        self._recalibrate_timer = threading.Timer(
            self._recalibrate_interval,
            self._auto_recalibrate
        )
        self._recalibrate_timer.daemon = True
        self._recalibrate_timer.start()

    def _auto_recalibrate(self):
        """Recalibra solo si no hay música sonando."""
        if not self._is_music_playing:
            print("Auto-recalibrating threshold...")
            new_threshold = calibrate()
            self.threshold = new_threshold
            print(f"Threshold updated: {new_threshold:.4f}")
        else:
            print("Skipping recalibration — music is playing")
        self._schedule_recalibration()  # programar la siguiente

    def _callback(self, indata, frames, time, status):
        """Process incoming audio data."""
        if status:
            print(f"Stream status: {status}")

        # Calculate RMS energy
        energy = np.sqrt(np.mean(indata ** 2))

        if self.verbose:
            print(f"Energy: {energy:.4f}")

        # Detect sudden spike: current energy must be X times the previous energy
        spike_ratio = energy / (self.prev_energy + 0.001)  # avoid division by zero
        is_clap = energy > self.threshold and spike_ratio > 2.0

        self.prev_energy = energy

        if is_clap:
            current_time = time_module.monotonic()
            self.detector.detect(current_time)

    def start(self):
        """Start listening for audio input."""
        self.stream = sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            blocksize=config.CHUNK_SIZE,
            channels=1,
            device=config.DEVICE_INDEX,
            callback=self._callback
        )
        self.stream.start()
        self._schedule_recalibration()

    def stop(self):
        """Stop listening for audio input."""
        if self._recalibrate_timer:
            self._recalibrate_timer.cancel()
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

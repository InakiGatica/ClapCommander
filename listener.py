import sounddevice as sd
import numpy as np
import time as time_module
import config
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
        """
        Args:
            on_double_clap: Callback for double clap.
            on_triple_clap: Callback for triple clap.
            verbose: If True, print detected energy values.
            threshold: Custom energy threshold. If None, uses config.ENERGY_THRESHOLD.
        """
        self.verbose = verbose
        self.detector = GestureEngine(
            on_double_clap=on_double_clap,
            on_triple_clap=on_triple_clap
        )
        self.stream = None
        self.threshold = threshold if threshold is not None else config.ENERGY_THRESHOLD
        self.prev_energy = 0.0

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

    def stop(self):
        """Stop listening for audio input."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

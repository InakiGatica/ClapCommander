import sounddevice as sd
import numpy as np
import time as time_module
import config
from detector import ClapDetector


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
    threshold = rms * 15  # safe margin

    print(f"Calibration done. Threshold set to: {threshold:.4f}")
    return threshold


class AudioListener:
    """Listens for audio input and detects claps."""

    def __init__(self, on_double_clap, verbose=False, threshold=None):
        """
        Args:
            on_double_clap: Callback function to call when double clap is detected.
            verbose: If True, print detected energy values.
            threshold: Custom energy threshold. If None, uses config.ENERGY_THRESHOLD.
        """
        self.on_double_clap = on_double_clap
        self.verbose = verbose
        self.detector = ClapDetector()
        self.stream = None
        self.threshold = threshold if threshold is not None else config.ENERGY_THRESHOLD

    def _callback(self, indata, frames, time, status):
        """Process incoming audio data."""
        if status:
            print(f"Stream status: {status}")

        # Calculate RMS energy
        energy = np.sqrt(np.mean(indata ** 2))

        if self.verbose:
            print(f"Energy: {energy:.4f}")

        # Check if energy exceeds threshold
        if energy > self.threshold:
            current_time = time_module.monotonic()
            if self.detector.detect(current_time):
                if self.verbose:
                    print("Double clap detected!")
                self.on_double_clap()

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

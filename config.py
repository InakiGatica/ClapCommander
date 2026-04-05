# Configuration constants for clap detector

import settings

SAMPLE_RATE = 44100  # not user-configurable
CHUNK_SIZE = 1024    # not user-configurable
MIN_INTERVAL = settings.get("min_interval", 0.15)
MAX_INTERVAL = settings.get("max_interval", 1.0)
ENERGY_THRESHOLD = settings.get("energy_threshold", 0.15)
COOLDOWN = settings.get("cooldown", 1.5)
DEVICE_INDEX = settings.get("device_index", 2)
CALIBRATION_SECONDS = settings.get("calibration_seconds", 3)
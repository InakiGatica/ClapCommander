# Configuration constants for clap detector

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
MIN_INTERVAL = 0.15  # seconds
MAX_INTERVAL = 1.0   # seconds
ENERGY_THRESHOLD = 0.22  # starting value, will calibrate later
COOLDOWN = 1.5  # seconds of silence after detection
DEVICE_INDEX = 2  # USB PnP Sound Device (brazo mic)
CALIBRATION_SECONDS = 3

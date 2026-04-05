from collections import deque
import config


class ClapDetector:
    """Detects double claps based on timestamp intervals."""

    def __init__(self):
        self.timestamps = deque(maxlen=2)
        self.last_action_time = 0.0

    def detect(self, timestamp: float) -> bool:
        """
        Add a timestamp and check for double clap pattern.

        Args:
            timestamp: Unix timestamp when the clap occurred.

        Returns:
            True if double clap detected (two claps within MIN_INTERVAL to MAX_INTERVAL),
            False otherwise.
        """
        # Cooldown check: ignore claps too close to last action
        if timestamp - self.last_action_time < config.COOLDOWN:
            return False

        self.timestamps.append(timestamp)

        # Need at least 2 claps to form a pattern
        if len(self.timestamps) < 2:
            return False

        # Calculate interval between the last two claps
        t1, t2 = self.timestamps[0], self.timestamps[1]
        interval = t2 - t1

        # Check if interval falls within the double clap window
        if config.MIN_INTERVAL <= interval <= config.MAX_INTERVAL:
            # Reset for next detection cycle
            self.last_action_time = timestamp
            self.timestamps.clear()
            return True

        return False

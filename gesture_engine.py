from collections import deque
import time as time_module
import config
import threading


class GestureEngine:
    """Detects double and triple clap patterns."""

    def __init__(self, on_double_clap=None, on_triple_clap=None):
        self.timestamps = deque(maxlen=3)
        self.last_action_time = 0.0
        self.on_double_clap = on_double_clap
        self.on_triple_clap = on_triple_clap
        self._pending_timer = None

    def detect(self, timestamp: float):
        """Process incoming clap timestamp."""
        # Cooldown check
        if timestamp - self.last_action_time < config.COOLDOWN:
            return

        self.timestamps.append(timestamp)

        # If 2 claps, start timer to confirm double
        if len(self.timestamps) == 2:
            t1, t2 = self.timestamps[0], self.timestamps[1]
            interval = t2 - t1

            if config.MIN_INTERVAL <= interval <= config.MAX_INTERVAL:
                # Start timer to confirm double clap
                self._pending_timer = threading.Timer(
                    config.MAX_INTERVAL,
                    self._confirm_double
                )
                self._pending_timer.start()

        # If 3 claps, cancel timer and confirm triple immediately
        elif len(self.timestamps) == 3:
            if self._pending_timer:
                self._pending_timer.cancel()
                self._pending_timer = None
            self._confirm_triple()

    def _confirm_double(self):
        """Confirm double clap pattern."""
        if len(self.timestamps) == 2:
            if self.on_double_clap:
                self.on_double_clap()
            self.last_action_time = time_module.monotonic()
            self.timestamps.clear()

    def _confirm_triple(self):
        if len(self.timestamps) < 3:
            self.timestamps.clear()
            return

        t1, t2, t3 = self.timestamps[0], self.timestamps[1], self.timestamps[2]
        interval1 = t2 - t1
        interval2 = t3 - t2

        # All intervals must be within valid clap range
        if (config.MIN_INTERVAL <= interval1 <= config.MAX_INTERVAL and
            config.MIN_INTERVAL <= interval2 <= config.MAX_INTERVAL):
            if self.on_triple_clap:
                self.on_triple_clap()
            self.last_action_time = time_module.monotonic()

        self.timestamps.clear()
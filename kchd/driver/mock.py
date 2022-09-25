"""Log the changes in LEDs."""
import logging
from typing import Dict, Set

from kchd.hardware import KCHLED
from kchd.types import KCHInfo

from .driver import LEDDriver

LOGGER = logging.getLogger(__name__)


class MockDriver(LEDDriver):
    """Log the changes in LEDs."""

    def __init__(self, leds: Set[KCHLED]) -> None:
        self._state: Dict[KCHLED, bool] = {led: False for led in leds}
        LOGGER.info(f"Initialised {len(leds)} LEDs with Mock Driver.")

    def get_kch_info(self) -> KCHInfo:
        """
        Get information about the KCH on the Pi.

        :raises NoKCHException: There is no KCH fitted.
        """
        return KCHInfo(
            vendor="Student Robotics",
            product="Mock KCH",
            asset_code="FAKE",
        )

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the LEDs state."""
        # Update the state
        old_state = self._state
        self._state = state

        # Log the changes
        for led, current_state in old_state.items():
            new_state = state[led]
            if new_state is not current_state:
                LOGGER.info(
                    f"{KCHLED(led).name} changed from {current_state} to {new_state}",
                )

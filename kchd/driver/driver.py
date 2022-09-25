"""Protocol for a class that can control the LEDs."""

from typing import Dict, Protocol, Set

from kchd.hardware import KCHLED


class LEDDriver(Protocol):
    """Protocol for a class that can control the LEDs."""

    def __init__(self, leds: Set[KCHLED]) -> None:
        """Initialise and set up the LEDs."""
        ...

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the state of the LEDs."""
        ...

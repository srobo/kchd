"""Protocol for a class that can control the LEDs."""

from typing import Dict, Protocol, Set

from kchd.hardware import KCHLED
from kchd.types import KCHInfo


class LEDDriver(Protocol):
    """Protocol for a class that can control the LEDs."""

    def __init__(self, leds: Set[KCHLED]) -> None:
        """Initialise and set up the LEDs."""
        ...

    def get_kch_info(self) -> KCHInfo:
        """
        Get information about the KCH this driver operates.

        :raises NoKCHException: There is no KCH available.
        """
        ...

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the state of the LEDs."""
        ...

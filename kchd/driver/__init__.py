"""Drivers for controlling the LEDs."""

from typing import Set

from kchd.hardware import KCHLED

from .driver import LEDDriver
from .gpio import GPIODriver


def get_driver(leds: Set[KCHLED]) -> LEDDriver:
    """Get the driver to use."""
    return GPIODriver(leds)


__all__ = ["get_driver", "GPIODriver", "LEDDriver"]

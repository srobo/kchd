"""Drivers for controlling the LEDs."""

from typing import Set

from kchd.hardware import KCHLED
from kchd.types import NoKCHException

from .driver import LEDDriver
from .gpio import GPIODriver
from .mock import MockDriver


def get_driver(leds: Set[KCHLED]) -> LEDDriver:
    """Get the driver to use."""
    for driver_cls in (GPIODriver, MockDriver):
        driver = driver_cls(leds)
        try:
            driver.get_kch_info()
            return driver
        except NoKCHException:
            pass
    raise RuntimeError("No drivers were available.")


__all__ = ["get_driver", "GPIODriver", "LEDDriver", "MockDriver"]

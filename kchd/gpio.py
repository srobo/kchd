"""Control the GPIO."""
import atexit
from typing import Dict

import RPi.GPIO as GPIO

from .hardware import KCHLED


class GPIOController:
    """Implementation of hardware LEDs."""

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  # Ignore that the BOOT_20 and BOOT_40 LEDs were in use.
        GPIO.setup([p.value for p in KCHLED], GPIO.OUT, initial=GPIO.LOW)
        atexit.register(GPIO.cleanup)

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the LEDs state."""
        for led, val in state.items():
            GPIO.output(led.value, GPIO.HIGH if val else GPIO.LOW)

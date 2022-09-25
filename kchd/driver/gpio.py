"""Control the LEDs using the RPi GPIO."""
import atexit
from typing import Dict, Set

import RPi.GPIO as GPIO

from kchd.hardware import KCHLED

from .driver import LEDDriver


class GPIODriver(LEDDriver):
    """Control the LEDs using the RPi GPIO."""

    def __init__(self, leds: Set[KCHLED]) -> None:
        self._leds = leds

        atexit.register(GPIO.cleanup)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup([led.value for led in self._leds], GPIO.OUT, initial=GPIO.LOW)

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the LEDs state."""
        if not set(state.keys()).issubset(self._leds):
            unknown_leds = state.keys() - self._leds
            raise ValueError(f"Some LEDs are not controlled by kchd: {unknown_leds}")

        for led, val in state.items():
            GPIO.output(led.value, GPIO.HIGH if val else GPIO.LOW)

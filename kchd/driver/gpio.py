"""Control the LEDs using the RPi GPIO."""
import atexit
from pathlib import Path
from typing import Dict, Set

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    GPIO = None  # type: ignore

from kchd.hardware import KCHLED
from kchd.types import KCHInfo, NoKCHException

from .driver import LEDDriver


class GPIODriver(LEDDriver):
    """Control the LEDs using the RPi GPIO."""

    DEVICE_TREE_SYS_PATH = Path("/sys/firmware/devicetree/base/hat")

    def __init__(self, leds: Set[KCHLED]) -> None:
        self._leds = leds

        if GPIO is not None:
            atexit.register(GPIO.cleanup)

            GPIO.setmode(GPIO.BCM)
            GPIO.setup([led.value for led in self._leds], GPIO.OUT, initial=GPIO.LOW)

    def _read_file(self, path: Path) -> str:
        if not path.exists() or not path.is_file():
            raise NoKCHException("SysFS is not readable.")

        with path.open("r") as fh:
            data = fh.read()
            data = data.rstrip("\x00")  # Null Terminated
            return data.strip()

    def get_kch_info(self) -> KCHInfo:
        """
        Get information about the KCH on the Pi.

        :raises NoKCHException: There is no KCH fitted.
        """
        sys_path = self.DEVICE_TREE_SYS_PATH

        if not sys_path.exists() or not sys_path.is_dir():
            raise NoKCHException("There is no HAT directory in sysfs.")

        vendor = self._read_file(sys_path / "vendor")
        product = self._read_file(sys_path / "product")

        if vendor == "Student Robotics" and product == "KCH V1 Rev B":
            return KCHInfo(
                vendor=vendor,
                product=product,
                asset_code=self._read_file(sys_path / "custom_0"),
            )
        else:
            raise NoKCHException("A HAT is fitted, but it is not a KCH.")

    def set_state(self, state: Dict[KCHLED, bool]) -> None:
        """Set the LEDs state."""
        if not set(state.keys()).issubset(self._leds):
            unknown_leds = state.keys() - self._leds
            raise ValueError(f"Some LEDs are not controlled by kchd: {unknown_leds}")

        for led, val in state.items():
            GPIO.output(led.value, GPIO.HIGH if val else GPIO.LOW)

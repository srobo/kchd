"""LED Controller Base Class."""

from abc import ABCMeta, abstractmethod
from typing import Callable, Coroutine, Dict, List

from astoria.common.mqtt.wrapper import MQTTWrapper

from kchd.hardware import KCHLED


class LEDController(metaclass=ABCMeta):
    """
    LED Controller.

    An LED Controller is responsible for the state of a group of LEDs.
    """

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        pass

    @property
    @abstractmethod
    def _leds(self) -> List[KCHLED]:
        """The LEDs that this controller is responsible for."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        raise NotImplementedError  # pragma: nocover

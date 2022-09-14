"""LED Controllers."""

import logging
from typing import Callable, Coroutine, Dict, Tuple

from astoria.common.ipc import RequestResponse
from astoria.common.mqtt.wrapper import MQTTWrapper

from kchd.hardware import KCHLED
from kchd.types import KCHLEDUpdateManagerRequest

from .controller import LEDController

LOGGER = logging.getLogger(__name__)


class MQTTRequestController(LEDController):
    """
    LED Controller for the Comp LED.

    It determines the state of the LEDs based on the requested state.
    """

    leds = [
        KCHLED.USER_A_RED,
        KCHLED.USER_A_GREEN,
        KCHLED.USER_A_BLUE,
        KCHLED.USER_B_RED,
        KCHLED.USER_B_GREEN,
        KCHLED.USER_B_BLUE,
        KCHLED.USER_C_RED,
        KCHLED.USER_C_GREEN,
        KCHLED.USER_C_BLUE,
        KCHLED.START,
    ]

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        self._mqtt = mqtt
        self._update_coro = update_coro

        self._a: Tuple[bool, bool, bool] = (False, False, False)
        self._b: Tuple[bool, bool, bool] = (False, False, False)
        self._c: Tuple[bool, bool, bool] = (False, False, False)
        self._start: bool = False

    async def handle_led_update(
            self,
            request: KCHLEDUpdateManagerRequest,
    ) -> RequestResponse:
        """Handle an LED Update Request."""
        self._a = request.a
        self._b = request.b
        self._c = request.c
        self._start = request.start
        await self._update_coro()
        return RequestResponse(uuid=request.uuid, success=True)

    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        a_red, a_green, a_blue = self._a
        b_red, b_green, b_blue = self._b
        c_red, c_green, c_blue = self._c
        return {
            KCHLED.USER_A_RED: a_red,
            KCHLED.USER_A_GREEN: a_green,
            KCHLED.USER_A_BLUE: a_blue,
            KCHLED.USER_B_RED: b_red,
            KCHLED.USER_B_GREEN: b_green,
            KCHLED.USER_B_BLUE: b_blue,
            KCHLED.USER_C_RED: c_red,
            KCHLED.USER_C_GREEN: c_green,
            KCHLED.USER_C_BLUE: c_blue,
            KCHLED.START: self._start,
        }

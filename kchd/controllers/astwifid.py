"""LED Controllers."""

import logging
from json import JSONDecodeError, loads
from typing import Callable, Coroutine, Dict, Match

from astoria.common.ipc import WiFiManagerMessage
from astoria.common.mqtt.wrapper import MQTTWrapper
from pydantic import ValidationError, parse_obj_as

from kchd.hardware import KCHLED

from .controller import LEDController

LOGGER = logging.getLogger(__name__)


class AstwifidController(LEDController):
    """
    LED Controller for the Code and OK LEDs.

    It determines the state of the LEDs based on the astwifid state.
    """

    leds = [KCHLED.WIFI]

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        self._mqtt = mqtt
        self._update_coro = update_coro

        self._mqtt.subscribe("astwifid", self.handle_astwifid_manager_message)

        # Assume not running to start with
        self._hotspot_running = False

    async def handle_astwifid_manager_message(
        self,
        match: Match[str],
        payload: str,
    ) -> None:
        """Event handler for astwifid state changes."""
        if payload:
            try:
                data = loads(payload)
                manager_message = parse_obj_as(WiFiManagerMessage, data)
                self._hotspot_running = manager_message.hotspot_running
                await self._update_coro()
            except ValidationError:
                LOGGER.warning("Received bad manager message.")
            except JSONDecodeError:
                LOGGER.warning("Received bad JSON in manager message.")
        else:
            LOGGER.warning("Received empty manager message.")

    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        return {
            KCHLED.WIFI: self._hotspot_running,
        }

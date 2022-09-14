"""LED Controllers."""

import logging
from json import JSONDecodeError, loads
from typing import Callable, Coroutine, Dict, Match, Optional, Tuple

from astoria.common.code_status import CodeStatus
from astoria.common.ipc import ProcessManagerMessage
from astoria.common.mqtt.wrapper import MQTTWrapper
from pydantic import ValidationError, parse_obj_as

from kchd.hardware import KCHLED

from .controller import LEDController

LOGGER = logging.getLogger(__name__)


class AstprocdController(LEDController):
    """
    LED Controller for the Code and OK LEDs.

    It determines the state of the LEDs based on the astprocd state.
    """

    leds = [KCHLED.STATUS_RED, KCHLED.STATUS_GREEN, KCHLED.STATUS_BLUE, KCHLED.CODE]

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        self._mqtt = mqtt
        self._update_coro = update_coro

        self._mqtt.subscribe("astprocd", self.handle_astprocd_manager_message)

        self._code: bool = False
        self._status: Optional[CodeStatus] = None

    async def handle_astprocd_manager_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for astprocd state changes."""
        if payload:
            try:
                data = loads(payload)
                manager_message = parse_obj_as(ProcessManagerMessage, data)
                self._code = manager_message.disk_info is not None
                self._status = manager_message.code_status
                await self._update_coro()
            except ValidationError:
                LOGGER.warning("Received bad manager message.")
            except JSONDecodeError:
                LOGGER.warning("Received bad JSON in manager message.")
        else:
            LOGGER.warning("Received empty manager message.")

    def get_led_status_from_code_status(
        self,
        status: Optional[CodeStatus],
    ) -> Tuple[bool, bool, bool]:
        """Get the RGB state of the OK LED from a CodeStatus."""
        status_map = {
            CodeStatus.STARTING: (False, True, True),  # Cyan
            CodeStatus.RUNNING: (True, True, False),  # Yellow
            CodeStatus.KILLED: (True, False, True),  # Magenta
            CodeStatus.FINISHED: (False, True, False),  # Green
            CodeStatus.CRASHED: (True, False, False),  # Red
            None: (False, False, False),  # Off
        }
        return status_map[status]

    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        red, green, blue = self.get_led_status_from_code_status(self._status)
        return {
            KCHLED.CODE: self._code,
            KCHLED.STATUS_RED: red,
            KCHLED.STATUS_GREEN: green,
            KCHLED.STATUS_BLUE: blue,
        }

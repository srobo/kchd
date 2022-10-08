"""LED Controllers."""

import logging
from json import JSONDecodeError, loads
from typing import Callable, Coroutine, Dict, Match, Optional

from astoria.common.ipc import MetadataManagerMessage
from astoria.common.metadata import RobotMode
from astoria.common.mqtt.wrapper import MQTTWrapper
from pydantic import ValidationError, parse_obj_as

from kchd.hardware import KCHLED

from .controller import LEDController

LOGGER = logging.getLogger(__name__)


class AstmetadController(LEDController):
    """
    LED Controller for the Comp LED.

    It determines the state of the LEDs based on the astmetad state.
    """

    leds = [KCHLED.COMP]

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        self._mqtt = mqtt
        self._update_coro = update_coro

        self._mqtt.subscribe("astmetad", self.handle_astmetad_manager_message)

        self._mode: Optional[RobotMode] = None

    async def handle_astmetad_manager_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for astprocd state changes."""
        if payload:
            try:
                data = loads(payload)
                manager_message = parse_obj_as(MetadataManagerMessage, data)
                if manager_message.metadata.mode != self._mode:
                    self._mode = manager_message.metadata.mode
                    LOGGER.info(f"Robot Mode has changed to {self._mode}")
                    await self._update_coro()
            except ValidationError as e:
                LOGGER.warning("Received bad manager message from astmetad.")
                LOGGER.warning(str(e))
            except JSONDecodeError as e:
                LOGGER.warning("Received bad JSON in astmetad manager message.")
                LOGGER.warning(str(e))
        else:
            LOGGER.warning("Received empty manager message from astmetad.")

    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        return {
            KCHLED.COMP: self._mode is RobotMode.COMP,
        }

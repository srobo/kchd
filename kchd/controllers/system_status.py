"""LED Controllers."""

import logging
from json import JSONDecodeError, loads
from typing import Callable, Coroutine, Dict, Match, Set

from astoria.common.ipc import ManagerMessage
from astoria.common.mqtt.wrapper import MQTTWrapper
from pydantic import ValidationError, parse_obj_as

from kchd.hardware import KCHLED

from .controller import LEDController

LOGGER = logging.getLogger(__name__)


class SystemStatusController(LEDController):
    """
    LED Controller for the System Status.

    This controller is responsible for the kchd controlled
    boot progress LEDs.

    It determines the state of the LEDs based on two input sources:

    1. The values of self.kchd_running, and self.mqtt_up. These values
    can be adjusted as a public attribute on the class, but
    update_leds must be invoked manually afterwards.

    2. It listens to all manager messages on the MQTT broker. If all of the
    required astoria managers are running, it will turn on an LED.
    """

    leds = [
        KCHLED.BOOT_20,
        KCHLED.BOOT_40,
        KCHLED.BOOT_60,
        KCHLED.BOOT_80,
        KCHLED.BOOT_100,
    ]
    _required_services = {"astdiskd", "astmetad", "astprocd"}

    def __init__(
        self,
        mqtt: MQTTWrapper,
        update_coro: Callable[[], Coroutine[None, None, None]],
    ) -> None:
        self._mqtt = mqtt
        self._update_coro = update_coro

        self.kchd_running: bool = False
        self.mqtt_up: bool = False
        self._seen_services: Set[str] = set()

        self._mqtt.subscribe("+", self.handle_manager_message)

    async def handle_manager_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for metadata changes."""
        if payload:
            try:
                data = loads(payload)
                manager_name = match.group(1)
                manager_message = parse_obj_as(ManagerMessage, data)
                if manager_name in self._required_services:
                    if manager_message.status is ManagerMessage.Status.RUNNING:
                        LOGGER.info(f"{manager_name} is running.")
                        self._seen_services |= {manager_name}
                    else:
                        LOGGER.info(f"{manager_name} is stopped.")
                        self._seen_services -= {manager_name}
                    await self._update_coro()
            except ValidationError:
                LOGGER.warning("Received bad manager message.")
            except JSONDecodeError:
                LOGGER.warning("Received bad JSON in manager message.")
        else:
            LOGGER.warning("Received empty manager message.")

    @property
    def astoria_good(self) -> bool:
        """Determine whether astoria services are in a good state."""
        return len(self._seen_services) == len(self._required_services)

    def get_enabled_leds(self) -> int:
        """Get the number of LEDs that should be enabled."""
        led_factors = [
            self.kchd_running,
            self.mqtt_up,
            self.astoria_good,
        ]
        return sum([1 for factor in led_factors if factor])

    def get_state(self) -> Dict[KCHLED, bool]:
        """Get the state of controlled LEDs."""
        leds_on = self.get_enabled_leds() + 2
        return {
            led: leds_on >= i + 1
            for i, led in enumerate(self.leds)
        }

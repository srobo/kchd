"""kchd - KCH LED Controller."""
import asyncio
import logging
from typing import Dict

from astoria.common.components import StateManager

from kchd.hardware import KCHLED

from .controllers import SystemStatusController
from .types import ControllerDictionary, KCHManagerMessage

LOGGER = logging.getLogger(__name__)


class KCHDaemon(StateManager[KCHManagerMessage]):
    """KCH LED Controller Daemon."""

    name = "kchd"

    def _init(self) -> None:
        self._lock = asyncio.Lock()

        self._controllers: ControllerDictionary = {
            "status": SystemStatusController(self._mqtt, self.update_leds),
        }

    async def main(self) -> None:
        """Main loop and entrypoint."""
        self.status = KCHManagerMessage(
            status=KCHManagerMessage.Status.RUNNING,
        )
        await self.wait_loop()

    @property
    def offline_status(self) -> KCHManagerMessage:
        """
        Status to publish when the manager goes offline.

        This status should ensure that any other components relying
        on this data go into a safe state.
        """
        return KCHManagerMessage(
            status=KCHManagerMessage.Status.STOPPED,
        )

    async def update_leds(self) -> None:
        """Update the LEDs on the KCH."""
        async with self._lock:
            state: Dict[KCHLED, bool] = {}
            for controller in self._controllers.values():
                partial_state = controller.get_state()  # type: ignore
                if partial_state.keys() & state.keys():
                    LOGGER.warning(
                        "Multiple controllers returned the same LED.",
                    )
                state.update(partial_state)
            LOGGER.debug(f"Current state: {state}")

    async def _pre_connect(self) -> None:
        """Before connecting to MQTT, we turn on 60% boot."""
        LOGGER.info("kchd is live.")
        self._controllers["status"].kchd_running = True
        await self.update_leds()

    async def _post_connect(self) -> None:
        """After connecting to MQTT, we turn on 80% boot."""
        LOGGER.info("Connected to Event Broker")
        self._controllers["status"].mqtt_up = True
        await self.update_leds()

    async def _post_disconnect(self) -> None:
        """Before connecting to MQTT, we turn on 60% boot."""
        LOGGER.info("Disconnecting, turn off all LEDs.")

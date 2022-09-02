"""
KCH daemon.

Manages the LEDs on the KCH board.
"""
import asyncio
import logging
from typing import Match

from astoria.common.components import StateConsumer

LOGGER = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


class KchControlDaemon(StateConsumer):
    """
    KCH control daemon.

    Updates the state of the KCH board's LEDs based on astoria events.
    """

    name = "kchd"

    def _init(self) -> None:
        self._mqtt.subscribe("astmetad", self.handle_astmetad_message)

    async def handle_astmetad_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for metadata changes."""
        pass

    async def handle_astprocd_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for process manager messages."""
        pass


if __name__ == '__main__':
    kchd = KchControlDaemon(False, None)
    loop.run_until_complete(kchd.run())

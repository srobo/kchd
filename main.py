"""
KCH daemon.

Manages the LEDs on the KCH board.
"""
import asyncio
import atexit
import logging
from json import loads
from typing import Match, Optional

import click
from astoria.common.components import StateConsumer
from astoria.common.disks import DiskType
from astoria.common.ipc import DiskManagerMessage, MetadataManagerMessage, ProcessManagerMessage
from astoria.common.metadata import RobotMode

from leds import AstoriaLEDs

LOGGER = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


@click.command("astwifid")
@click.option("-v", "--verbose", is_flag=True)
@click.option("-c", "--config-file", type=click.Path(exists=True))
def main(*, verbose: bool, config_file: Optional[str]) -> None:
    kchd = KchControlDaemon(verbose, config_file)
    loop.run_until_complete(kchd.run())


try:
    import RPi.GPIO as GPIO
except ImportError:
    # Stubbed class for the output functions
    class GPIO():  # type: ignore
        BCM = 11
        BOARD = 10
        BOTH = 33
        FALLING = 32
        HARD_PWM = 43
        HIGH = 1
        I2C = 42
        IN = 1
        LOW = 0
        OUT = 0
        PUD_DOWN = 21
        PUD_OFF = 20
        PUD_UP = 22
        RISING = 31
        RPI_INFO = ''
        RPI_REVISION = 3
        SERIAL = 40
        SPI = 41
        UNKNOWN = -1
        VERSION = '0.0.0'

        @classmethod
        def cleanup(cls, channel=None):
            pass

        @classmethod
        def gpio_function(cls, channel):
            return cls.IN

        @classmethod
        def output(cls, channel, value):
            LOGGER.info(f"Setting pin {channel} to {value}")

        @classmethod
        def setmode(cls, mode):
            pass

        @classmethod
        def setup(cls, channel, direction, pull_up_down=None, initial=None):
            pass

        @classmethod
        def setwarnings(cls, enable):
            pass

        class PWM:
            def __init__(self, channel, frequency):
                pass

            def ChangeDutyCycle(self, dutycylce):
                pass

            def ChangeFrequency(self, frequency):
                pass

            def start(self, dutycycle):
                pass

            def stop(self):
                pass


class KchControlDaemon(StateConsumer):
    """
    KCH control daemon.

    Updates the state of the KCH board's LEDs based on astoria events.
    """

    name = "kchd"

    def _init(self) -> None:
        self._mqtt.subscribe("astdiskd", self.handle_astdiskd_message)
        self._mqtt.subscribe("astmetad", self.handle_astmetad_message)
        self._mqtt.subscribe("astprocd", self.handle_astprocd_message)

    async def main(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AstoriaLEDs.all(), GPIO.OUT, initial=GPIO.LOW)
        atexit.register(GPIO.cleanup)

        await self.wait_loop()

    async def handle_astdiskd_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for metadata changes."""
        message: DiskManagerMessage = DiskManagerMessage(**loads(payload))
        if message.status == DiskManagerMessage.Status.RUNNING:
            has_usercode = any(
                disk.disk_type == DiskType.USERCODE
                for disk in message.calculate_disk_info(self.config.astprocd.default_usercode_entrypoint).values()
            )
            if has_usercode:
                GPIO.output(AstoriaLEDs.CODE, GPIO.HIGH)
                return
        GPIO.output(AstoriaLEDs.CODE, GPIO.LOW)

    async def handle_astmetad_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for metadata changes."""
        message: MetadataManagerMessage = MetadataManagerMessage(**loads(payload))
        if message.status == MetadataManagerMessage.Status.RUNNING:
            if message.metadata.mode == RobotMode.COMP:
                GPIO.output(AstoriaLEDs.COMP, GPIO.HIGH)
        GPIO.output(AstoriaLEDs.COMP, GPIO.LOW)

    async def handle_astprocd_message(
            self,
            match: Match[str],
            payload: str,
    ) -> None:
        """Event handler for process manager messages."""
        message: ProcessManagerMessage = ProcessManagerMessage(**loads(payload))
        if message.status == ProcessManagerMessage.Status.RUNNING:
            pass
        # TODO: Reset here


if __name__ == '__main__':
    main()

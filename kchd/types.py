"""Type definitions."""
from typing import TypedDict

from astoria.common.ipc import ManagerMessage

from .controllers import SystemStatusController


class KCHManagerMessage(ManagerMessage):
    """
    Status Manager for KCH Daemon.

    Published to astoria/kchd
    """


class ControllerDictionary(TypedDict):
    """
    The dictionary of LED Controllers.

    Mypy is not currently clever enough to tell that
    all of these are a subclass of LEDController.
    """

    status: SystemStatusController

"""Type definitions."""
from typing import TYPE_CHECKING, Optional, Tuple, TypedDict
from uuid import UUID

from astoria.common.ipc import ManagerMessage, ManagerRequest
from pydantic import BaseModel

if TYPE_CHECKING:
    from .controllers import (
        AstmetadController,
        AstprocdController,
        MQTTRequestController,
        SystemStatusController,
    )


class KCHInfo(BaseModel):
    """Information about the KCH."""

    vendor: str
    product: str
    asset_code: str
    uuid: UUID


class KCHManagerMessage(ManagerMessage):
    """
    Status Manager for KCH Daemon.

    Published to astoria/kchd
    """

    kch: Optional[KCHInfo] = None


class KCHLEDUpdateManagerRequest(ManagerRequest):
    """A request to change the controllable LEDs."""

    start: bool = False
    a: Tuple[bool, bool, bool] = (False, False, False)
    b: Tuple[bool, bool, bool] = (False, False, False)
    c: Tuple[bool, bool, bool] = (False, False, False)


class ControllerDictionary(TypedDict):
    """
    The dictionary of LED Controllers.

    Mypy is not currently clever enough to tell that
    all of these are a subclass of LEDController.
    """

    astmetad: 'AstmetadController'
    astprocd: 'AstprocdController'
    mqtt: 'MQTTRequestController'
    status: 'SystemStatusController'

"""Get information about the KCH."""
from pathlib import Path

from .types import KCHInfo

DEVICE_TREE_SYS_PATH = Path("/sys/firmware/devicetree/base/hat")


class NoKCHException(Exception):
    """There is no KCH on the Pi."""


def _read_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise NoKCHException("SysFS is not readable.")

    with path.open("r") as fh:
        data = fh.read()
        data = data.rstrip("\x00")  # Null Terminated
        return data.strip()


def get_kch_info(*, sys_path: Path = DEVICE_TREE_SYS_PATH) -> KCHInfo:
    """
    Get information about the KCH on the Pi.

    :raises NoKCHException: There is no KCH fitted.
    """
    if not sys_path.exists() or not sys_path.is_dir():
        raise NoKCHException("There is no HAT directory in sysfs.")

    vendor = _read_file(sys_path / "vendor")
    product = _read_file(sys_path / "product")

    if vendor == "Student Robotics" and product == "KCH V1 Rev B":
        return KCHInfo(
            vendor=vendor,
            product=product,
            asset_code=_read_file(sys_path / "custom_0"),
        )
    else:
        raise NoKCHException("A HAT is fitted, but it is not a KCH.")

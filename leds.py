from enum import unique, IntEnum


@unique
class AstoriaLEDs(IntEnum):
    # BOOT_20 = 7  # Managed by kernel
    # BOOT_40 = 5  # Managed by systemd
    BOOT_60 = 12
    BOOT_80 = 6
    BOOT_100 = 13

    CODE = 11
    COMP = 16

    WIFI = 8
    # HEARTBEAT = 19  # Managed by device-tree

    STATUS_RED = 26
    STATUS_GREEN = 20
    STATUS_BLUE = 21

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))

"""Hardware definitions."""
import enum


@enum.unique
class KCHLED(enum.IntEnum):
    """
    All LEDs on the KCH.

    The value of each LED in the Enum is the BCM pin number.
    """

    BOOT_20 = 7
    BOOT_40 = 5
    BOOT_60 = 12
    BOOT_80 = 6
    BOOT_100 = 13

    CODE = 11
    COMP = 16

    HEARTBEAT = 19

    STATUS_RED = 26
    STATUS_GREEN = 20
    STATUS_BLUE = 21

    START = 9

    USER_A_RED = 24
    USER_A_GREEN = 10
    USER_A_BLUE = 25
    USER_B_RED = 27
    USER_B_GREEN = 23
    USER_B_BLUE = 22
    USER_C_RED = 4
    USER_C_GREEN = 18
    USER_C_BLUE = 17

    WIFI = 8

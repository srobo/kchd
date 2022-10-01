# kchd - KCH LED Controller Daemon

The [KCH][kch-hw] is a Raspberry Pi [HAT][hat] for the [Student Robotics][srobo] kit.

This program runs on the robot during student development and competitions and controls the LEDs on the KCH.

[hat]: https://www.raspberrypi.com/news/introducing-raspberry-pi-hats/
[kch-hw]: https://github.com/srobo/kch-hw
[rpi]: https://raspberrypi.org
[srobo]: https://studentrobotics.org

## Why does this exist?

The new KCH HAT that we're shipping with our brain boards have a number of LEDs on it, some of which are to indicate the state of the robot and some are user controlled.

### Controlling the State LEDs

The "state" of the robot is more specifically the state of the various state managers in our Astoria robot management system. Astoria handles events (such as a USB stick insertion) and publishes the information onto an MQTT event broker. In order to control the LEDs, we need to subscribe to the state messages on the event broker and set the LEDs appropriately when the state changes. This is implemented in a new daemon called kchd. If it were not exclusive to the SR kits, kchd would properly be part of Astoria.

### Controlling the User LEDs

At an initial glance, it would seem that we can drive the user LEDs directly from sr.robot3. Whilst we don't run usercode as root, we can configure permissions so that the usercode can control GPIO. However, we are unable to grant permissions at a level any more granular than this, usercode can control all of the GPIO or none. So that the debug LEDs on the HAT are actually reliably useful, we have intentionally chosen to restrict the usercode from controlling any of the user LEDs, instead controlling them via kchd.

This reason alone is perhaps not enough to introduce inter-process communication into toggling some LEDs, although it is also not the only reason that we need the user LEDs to be managed externally.

### Handling LEDs when Usercode exits

Typically, when a program controlling GPIO exits it is good practise to cleanup the GPIO so that it is available to other programs. This tends to result in the GPIO being turned off when it is reset. This is very much not desirable behaviour if we turn off the user LEDs when the usercode exits.

In fact the behaviour we want to see is:

- When usercode exits, the state of the user LEDs stays exactly the same.
- When the usercode USB is removed OR the usercode restarts, the User LEDs reset to be off.

This behaviour is only achievable using an external daemon as we need to listen to Astoria state messages to turn off the LEDs at the right time.

## LED Groups

There are 22 LEDs on the KCH that are connected to GPIO pins on the Raspberry Pi.

Of these, all but three are controlled by kchd.

All remaining LEDs are split into one of five LED Groups, detailed below:

### System Status

The top three boot progress LEDs are controlled by the system status:

- `BOOT_20`: Not controlled by kchd
- `BOOT_40`: Not controlled by kchd
- `BOOT_60`: Indicates that kchd is running
- `BOOT_80`: Indicates that the MQTT Event Broker is running, and that kchd has connected.
- `BOOT_100`: Indicates that the [Astoria](https://github.com/srobo/astoria) services have started and are running.

### User Controllable

Some LEDs are controlled by the usercode program on the robot.

Whilst it would be possible for them to be driven directly, kchd instead exposes a control interface over MQTT.

- `USER_A` - This is a user controlled RGB LED.
- `USER_B` - This is a user controlled RGB LED.
- `USER_C` - This is a user controlled RGB LED.
- `START` - Indicates that the Robot is ready to start.

### `astprocd`

The following LEDs are controlled based on the state of [`astprocd`](https://srobo.github.io/astoria/implementation/managers/astprocd.html).

- `CODE` - Lights up if a valid usercode drive is found.
- `OK` - RGB LED, colour is dependent on code status.

### `astmetad`

The following LEDs are controlled based on the state of [`astprocd`](https://srobo.github.io/astoria/implementation/managers/astmetad.html).

- `COMP` - The Robot is in [competition mode](https://srobo.github.io/astoria/implementation/managers/astmetad.html?highlight=comp#astoria.common.metadata.RobotMode).

### `astwifid`

The following LEDs are controlled based on the state of `astwifid`.

- `WIFI` - Lights up if the WiFi is enabled.

## LEDs not controlled by kchd

There are three LEDs that are not controlled by kchd.

- `HEARTBEAT` - The heartbeat LED is driven directly by the kernel and is set in device tree.
- `BOOT_20` - The 20% boot LED is also controlled by device tree.
- `BOOT_40` - The 40% boot LED is controlled by a systemd service at `basic.target`
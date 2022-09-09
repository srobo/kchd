# kchd - KCH LED Controller Daemon

The [KCH][kch-hw] is a Raspberry Pi [HAT][hat] for the [Student Robotics][srobo] kit.

This program runs on the robot during student development and competitions and controls the LEDs on the KCH.

[hat]: https://www.raspberrypi.com/news/introducing-raspberry-pi-hats/
[kch-hw]: https://github.com/srobo/kch-hw
[rpi]: https://raspberrypi.org
[srobo]: https://studentrobotics.org

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

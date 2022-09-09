"""KCH Daemon."""

import asyncio
import logging
from typing import Optional

import click

from .app import KCHDaemon

LOGGER = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


@click.command("kchd")
@click.option("-v", "--verbose", is_flag=True)
@click.option("-c", "--astoria-config-file", type=click.Path(exists=True))
def main(*, verbose: bool, astoria_config_file: Optional[str]) -> None:
    """KCH Daemon Application Entrypoint."""
    kchd = KCHDaemon(verbose, astoria_config_file)
    loop.run_until_complete(kchd.run())


if __name__ == "__main__":
    main()

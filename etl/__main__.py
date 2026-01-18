"""RP To-Do entry point script."""
import os
from pathlib import Path

from etl import cli, __app_name__
from etl.config import setup_ffmpeg


# Configurar FFmpeg
setup_ffmpeg()


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()

import argparse

from timebomb.app import App
from timebomb import __VERSION__, __DESCRIPTION__


def main():
    """Entry endpoint for CLI."""
    parser = argparse.ArgumentParser(description=__DESCRIPTION__)
    parser.add_argument("host", type=str, help="Time Bomb server address")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__VERSION__)
    )
    args = parser.parse_args()

    TA = App(host=args.host)
    TA.run()

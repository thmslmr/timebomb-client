import argparse

from timebomb.app import App


def main():
    """Entry endpoint for CLI."""
    parser = argparse.ArgumentParser(description="Time Bomb.")
    parser.add_argument("host", type=str, help="Time Bomb server address.")
    args = parser.parse_args()

    TA = App(host=args.host)
    TA.run()

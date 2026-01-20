"""CLI entry point for marketing service."""

import sys


def main():
    """Run the marketing service."""
    from .api import main as run_api
    run_api()


if __name__ == "__main__":
    main()

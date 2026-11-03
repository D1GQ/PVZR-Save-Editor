"""Entry point: `python -m pvzr_save_editor`."""

import sys


def run():
    try:
        from .ui.app import main
    except ImportError as e:  # most likely tkinter missing
        sys.stderr.write(f"Failed to start: {e}\n")
        raise
    main()


if __name__ == "__main__":
    run()

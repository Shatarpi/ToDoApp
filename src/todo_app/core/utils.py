# All of the below, except comments, was made with AI (all while thorougly explaining what each step does) as it was a new but required concept and library for the app to work.

import sys
import os

# --- PATH TO RESOURCES (assets etc.) ---
def resource_path(relative_path):
    try:
        # If PyInstaller variable exists, use that/it's path
            # It becomes available when runnning a packaged version of the app
        base_path = sys._MEIPASS # This "should" have a red squiggly line

    # Else, use the current working directory (ie when working in VS code)
    except Exception:
        base_path = os.path.abspath(".")

    # Return the combined path to resource
    return os.path.join(base_path, relative_path)
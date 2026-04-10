import os
import getpass
from pathlib import Path


def find_edge_profile():
    user = getpass.getuser()

    possible_paths = [
        f"C:/Users/{user}/AppData/Local/Microsoft/Edge/User Data",
        f"C:/Users/{user}/AppData/Local/Microsoft/Edge Beta/User Data",
        f"C:/Users/{user}/AppData/Local/Microsoft/Edge Dev/User Data",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            default_profile = os.path.join(path, "Default")

            if os.path.exists(default_profile):
                return path, "Default"

            # fallback: find any profile
            for folder in os.listdir(path):
                if folder.startswith("Profile"):
                    return path, folder

    raise Exception("Edge profile not found")
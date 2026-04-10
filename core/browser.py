import subprocess
import time

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from pathlib import Path

from core.profile import find_edge_profile
from config import KILL_EDGE_ON_START


def kill_edge():
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "msedge.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
    except:
        pass


def create_browser():
    if KILL_EDGE_ON_START:
        kill_edge()

    profile_path, profile_dir = find_edge_profile()
    driver_path = Path("drivers/msedgedriver.exe")

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_argument("--start-maximized")

    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    service = Service(driver_path)

    driver = webdriver.Edge(service=service, options=options)

    return driver
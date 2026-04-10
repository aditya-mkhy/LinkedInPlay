from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from pathlib import Path

from core.profile import find_edge_profile


def create_browser():
    profile_path, profile_dir = find_edge_profile()

    driver_path = Path("drivers/msedgedriver.exe")

    options = Options()

    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_dir}")

    options.add_argument("--start-maximized")

    # IMPORTANT FIX
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    service = Service(driver_path)

    driver = webdriver.Edge(service=service, options=options)

    return driver
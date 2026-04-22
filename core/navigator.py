import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


LINKEDIN_GAMES = "https://www.linkedin.com/games/"
ZIP_GAME = "https://www.linkedin.com/games/zip/"
PATCHES = "https://www.linkedin.com/games/patches/"
QUEENS = "https://www.linkedin.com/games/queens/"


def open_games_home(driver):
    driver.get(LINKEDIN_GAMES)
    print(f"Waiting for 10 Seconds....")
    time.sleep(10)

def open_zip(driver):
    open_game(driver, ZIP_GAME)

def open_patches(driver):
    open_game(driver, PATCHES)

def open_queens(driver):
    open_game(driver, QUEENS)

def open_game(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10, poll_frequency=0.05)

    # wait for page load (fastest baseline)
    wait.until(lambda d: d.execute_script(
        "return document.readyState"
    ) == "complete")

    # wait for actual game cells (REAL readiness)
    wait.until(lambda d: len(d.find_elements(
        By.CSS_SELECTOR,
        '[data-testid^="cell-"]'
    )) > 0)

    print("[READY] Zip grid loaded")
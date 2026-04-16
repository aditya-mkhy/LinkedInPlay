import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


LINKEDIN_GAMES = "https://www.linkedin.com/games/"
ZIP_GAME = "https://www.linkedin.com/games/zip/"


def open_games_home(driver):
    driver.get(LINKEDIN_GAMES)
    time.sleep(3)


def open_zip(driver):
    driver.get(ZIP_GAME)
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
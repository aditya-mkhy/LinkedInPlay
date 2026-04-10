import time


LINKEDIN_GAMES = "https://www.linkedin.com/games/"
ZIP_GAME = "https://www.linkedin.com/games/zip/"


def open_games_home(driver):
    driver.get(LINKEDIN_GAMES)
    time.sleep(3)


def open_zip(driver):
    driver.get(ZIP_GAME)
    time.sleep(3)
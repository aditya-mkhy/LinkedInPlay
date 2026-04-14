from core.browser import create_browser
from core.navigator import open_zip
from games.zip import ZipGame


def main():
    driver = create_browser()

    open_zip(driver)

    game = ZipGame(driver)
    game.play()

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
from core.browser import create_browser
from core.navigator import open_zip
from games.zip import ZipGame


def main():
    driver = create_browser()

    open_zip(driver)

    game = ZipGame(driver)
    # game.play()

    path = [21, 9, 10, 22, 24, 18, 17, 11, 12, 6, 1, 7, 8, 14, 13, 31, 32, 26, 27, 33, 34, 28, 29, 35, 36, 30]
    
    game.play_with_solution(path, is_start_with_0 = False)

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
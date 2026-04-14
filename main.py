from core.browser import create_browser
from core.navigator import open_zip
from games.zip import ZipGame


def main():
    driver = create_browser()

    open_zip(driver)

    game = ZipGame(driver)
    # game.play()

    path = [34, 35, 36, 30, 29, 28, 27, 21, 15, 14, 8, 9, 10, 22, 24, 18, 17, 11, 12, 6, 1, 19, 20, 26, 25, 31, 33]
    
    game.play_with_solution(path, is_start_with_0 = False)

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
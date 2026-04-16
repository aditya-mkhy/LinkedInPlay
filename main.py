from core.browser import create_browser
from core.navigator import open_zip
from games.zip import ZipGame


def main():
    driver = create_browser()

    open_zip(driver)

    game = ZipGame(driver)
    # game.play()

    path = [11, 17, 16, 22, 23, 29, 27, 33, 36, 6, 4, 10, 8, 14, 15, 21, 20,32, 31, 1, 3]
    
    game.play_with_solution(path, is_start_with_0 = False)

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
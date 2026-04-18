from core.browser import create_browser
from core.navigator import open_zip
from games.zip import ZipGame


def main():
    driver = create_browser()

    open_zip(driver)

    game = ZipGame(driver)

    if game.is_completed():
        print("[SKIP] Already played")
        return

    # game.play()


    path = [45, 49, 7, 6, 13, 12, 5, 1, 8, 11, 18, 20, 27,26, 33, 34, 41, 39, 25, 24, 17, 15, 43, 44, 23]
    
    game.play_with_solution(path, is_start_with_0 = False)

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
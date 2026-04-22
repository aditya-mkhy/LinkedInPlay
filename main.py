from core.browser import create_browser
from core.navigator import open_zip, open_games_home, open_patches, open_queens
from games.zip import ZipGame
from games.queens  import QueensGame



def main():
    driver = create_browser()
    open_games_home(driver)

    # open_zip(driver)
    open_queens(driver)

    game = QueensGame(driver)
    if game.is_completed():
        print("[SKIP] Already played")
        return
    
    game.play()

    # game = ZipGame(driver)

    # if game.is_completed():
    #     print("[SKIP] Already played")
    #     return


    # path = [30, 32, 25, 22, 43, 45, 38, 39, 46, 49, 42, 40, 19, 18, 11, 13, 34, 35, 7, 3, 10, 9, 2, 1, 15, 17]
    
    # game.play_with_solution(path, is_start_with_0 = False)

    confirmation = input("Press enter to quit....")


if __name__ == "__main__":
    main()
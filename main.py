from core.browser import create_browser
from core.navigator import open_zip


def main():
    driver = create_browser()

    open_zip(driver)

    input("Zip opened. Press Enter to exit...")
    driver.quit()


if __name__ == "__main__":
    main()
from selenium.webdriver.common.by import By
from games.base import BaseGame
import time


class ZipGame(BaseGame):

    def play(self):
        print("Zip bot started...")

        while True:
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")

                for b in buttons:
                    if self.is_game_button(b):
                        self.fast_click(b)

            except Exception:
                pass

    def is_game_button(self, element):
        try:
            text = element.text.strip().lower()

            # ignore UI buttons
            ignore = ["share", "copy", "close", "help", "settings"]

            if any(word in text for word in ignore):
                return False

            # must be visible & enabled
            if not element.is_displayed():
                return False

            return True

        except:
            return False

    def fast_click(self, element):
        try:
            self.driver.execute_script(
                "arguments[0].click();", element
            )
        except:
            pass
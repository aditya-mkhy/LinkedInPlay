from selenium.webdriver.common.by import By
from games.base import BaseGame


class ZipGame(BaseGame):

    def play(self):
        print("Smart Zip AI started...")

        while True:
            try:
                cells = self.get_clickable_cells()

                if not cells:
                    continue

                target = self.pick_next(cells)

                if target:
                    self.click(target)

            except Exception:
                pass

    def get_clickable_cells(self):
        cells = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[data-testid^="cell-"][role="button"]'
        )

        valid = []

        for c in cells:
            try:
                state = c.get_attribute("aria-describedby")

                # ignore already connected
                if state == "zip-cell-connected":
                    continue

                number = self.extract_number(c)

                if number is not None:
                    valid.append((number, c))

            except:
                continue

        return valid

    def extract_number(self, element):
        try:
            label = element.get_attribute("aria-label")
            # "Number 5" → 5
            return int(label.split(" ")[1])
        except:
            return None

    def pick_next(self, cells):
        # pick smallest number
        cells.sort(key=lambda x: x[0])
        return cells[0][1]

    def click(self, element):
        try:
            self.driver.execute_script(
                "arguments[0].click();", element
            )
        except:
            pass
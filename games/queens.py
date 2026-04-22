from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from games.base import BaseGame
import time
import re


class QueensGame(BaseGame):

    def __init__(self, driver):
        super().__init__(driver)
        self.size = 0
        self.cells = []

    # ==========================================
    # ENTRY
    # ==========================================
    def play(self):
        print("\n=== QUEENS SOLVER ===")

        self.parse_board()

        solution = self.solve()

        if not solution:
            print("[FAIL] No solution")
            return

        print("[SOLUTION]", solution)

        self.execute(solution)

    # ==========================================
    # PARSE BOARD
    # ==========================================
    def parse_board(self):

        grid = self.driver.find_element(
            By.CSS_SELECTOR,
            '[data-testid="interactive-grid"]'
        )

        style = grid.get_attribute("style")

        m = re.search(r'--efd451f0:\s*(\d+)', style)
        self.size = int(m.group(1))

        print("[SIZE]", self.size)

        elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[data-testid^="cell-"]'
        )

        self.cells = []

        for el in elements:

            idx = int(el.get_attribute("data-cell-idx"))

            label = el.get_attribute("aria-label")

            # row / col
            row = idx // self.size
            col = idx % self.size

            # color / region
            color = "Unknown"

            m = re.search(r'color (.*?), row', label)
            if m:
                color = m.group(1)

            # queen already exists?
            has_queen = "Queen of color" in label

            self.cells.append({
                "idx": idx,
                "row": row,
                "col": col,
                "color": color,
                "queen": has_queen,
                "el": el
            })

    # ==========================================
    # SOLVER
    # ==========================================
    def solve(self):

        board = self.cells
        size = self.size

        row_map = {}
        for c in board:
            row_map.setdefault(c["row"], []).append(c)

        used_cols = set()
        used_regions = set()
        placed = []

        # preload queens if any
        for c in board:
            if c["queen"]:
                used_cols.add(c["col"])
                used_regions.add(c["color"])
                placed.append(c)

        def touching(r1, c1, r2, c2):
            return abs(r1-r2) <= 1 and abs(c1-c2) <= 1

        def backtrack(row):

            if row == size:
                return placed.copy()

            # skip row if already queen there
            if any(q["row"] == row for q in placed):
                return backtrack(row + 1)

            for cell in row_map[row]:

                if cell["col"] in used_cols:
                    continue

                if cell["color"] in used_regions:
                    continue

                bad = False

                for q in placed:
                    if touching(
                        cell["row"], cell["col"],
                        q["row"], q["col"]
                    ):
                        bad = True
                        break

                if bad:
                    continue

                # place
                placed.append(cell)
                used_cols.add(cell["col"])
                used_regions.add(cell["color"])

                result = backtrack(row + 1)

                if result:
                    return result

                # undo
                placed.pop()
                used_cols.remove(cell["col"])
                used_regions.remove(cell["color"])

            return None

        return backtrack(0)

    # ==========================================
    # EXECUTE
    # ==========================================
    def execute(self, solution):

        print("[PLAYING]")

        for cell in solution:

            if cell["queen"]:
                continue

            try:
                self.driver.execute_script(
                    "arguments[0].click();",
                    cell["el"]
                )

                time.sleep(0.03)

            except Exception as e:
                print("[ERROR]", e)
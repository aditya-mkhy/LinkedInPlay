from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from games.base import BaseGame
import time
import re
import random


class QueensGame(BaseGame):

    def __init__(self, driver):
        super().__init__(driver)
        self.size = 0
        self.cells = []

    def is_completed(self):
        try:
            elements = self.driver.find_elements(
                By.XPATH,
                "//span[contains(text(),'See results')]"
            )

            if elements:
                print("[INFO] Queens already completed")
                return True

            return False

        except Exception as e:
            print("[CHECK ERROR]", e)
            return False

    # PLAY
    def play(self, solve_in_sec=0, mistakes=False):
        print("\n=== QUEENS SOLVER ===")

        if self.is_completed():
            print("[SKIP] Already played today")
            return

        self.parse_board()

        solution = self.solve()

        if not solution:
            print("[FAIL] No solution")
            return

        print("[SOLUTION FOUND]")

        if solve_in_sec == 0:
            self.execute(solution)
        else:
            self.execute_smart(
                solution,
                total_time=solve_in_sec,
                mistakes=mistakes
            )


    # PARSE BOARD
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


    # SOLVER
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

    def execute(self, solution):
        print("[PLAYING BULLETPROOF]")


        for move_no, cell in enumerate(solution, start=1):

            idx = cell["idx"]

            # skip already queen
            if self.is_queen(idx):
                print(f"[SKIP] idx={idx} already queen")
                continue

            success = False

            for attempt in range(1, 4):

                try:
                    el = self.driver.find_element(
                        By.CSS_SELECTOR,
                        f'[data-cell-idx="{idx}"]'
                    )

                    print(
                        f"[MOVE {move_no}] "
                        f"idx={idx} "
                        f"(try {attempt})"
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        el
                    )

                    ActionChains(self.driver)\
                        .move_to_element(el)\
                        .pause(0.02)\
                        .click()\
                        .pause(0.05)\
                        .click()\
                        .perform()

                    time.sleep(0.08)

                    # verify
                    if self.is_queen(idx):
                        print(f"[OK] Queen placed at {idx}")
                        success = True
                        break
                    else:
                        print(f"[RETRY] Queen not detected at {idx}")

                except StaleElementReferenceException:
                    print("[STALE] Retrying...")

                except Exception as e:
                    print("[ERROR]", e)

            if not success:
                print(f"[FAIL] Could not place queen at {idx}")


    def execute_smart(self, solution, total_time=8, mistakes=False):
        print(f"[SMART MODE] target={total_time}s mistakes={mistakes}")


        start = time.time()

        moves = [c for c in solution if not c["queen"]]
        total_moves = len(moves)

        # reserve time for mistakes
        extra = 1.0 if mistakes else 0.0

        usable_time = max(1, total_time - extra)

        base_delay = usable_time / max(1, total_moves)

        # optional mistake slots
        mistake_turns = set()
        if mistakes and total_moves >= 4:
            count = random.randint(1, 2)
            while len(mistake_turns) < count:
                mistake_turns.add(random.randint(1, total_moves - 1))

        for i, cell in enumerate(moves, start=1):

            # fake mistake before real move
            if i in mistake_turns:
                self.fake_mistake()

            idx = cell["idx"]

            print(f"[MOVE {i}/{total_moves}] idx={idx}")

            self.place_queen(idx)

            # natural variable delay
            jitter = random.uniform(-0.20, 0.25) * base_delay
            delay = max(0.05, base_delay + jitter)

            time.sleep(delay)

        spent = time.time() - start

        # exact finish timing if early
        if spent < total_time:
            time.sleep(total_time - spent)

        print("[DONE SMART]")


    def place_queen(self, idx):

        for _ in range(3):

            if self.is_queen(idx):
                return

            el = self.driver.find_element(
                By.CSS_SELECTOR,
                f'[data-cell-idx="{idx}"]'
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                el
            )

            ActionChains(self.driver)\
                .move_to_element(el)\
                .pause(0.01)\
                .click()\
                .pause(0.03)\
                .click()\
                .perform()

            time.sleep(0.05)

            if self.is_queen(idx):
                return

    def is_queen(self, idx):
        try:
            el = self.driver.find_element(
                By.CSS_SELECTOR,
                f'[data-cell-idx="{idx}"]'
            )

            label = el.get_attribute("aria-label") or ""

            return "Queen of color" in label

        except:
            return False
        


    def fake_mistake(self):
        try:
            cells = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[data-testid^="cell-"]'
            )

            random.shuffle(cells)

            for el in cells[:10]:

                label = el.get_attribute("aria-label") or ""

                # only empty cells
                if "Empty cell" not in label:
                    continue

                print("[MISTAKE] fake X move")

                ActionChains(self.driver)\
                    .move_to_element(el)\
                    .pause(0.01)\
                    .click()\
                    .pause(0.25)\
                    .click()\
                    .perform()

                time.sleep(0.15)
                return

        except:
            pass
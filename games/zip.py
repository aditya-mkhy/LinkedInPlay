from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from games.base import BaseGame
import time


class ZipGame(BaseGame):

    def __init__(self, driver):
        super().__init__(driver)
        self.size = 6

    #auto mode
    def play(self):
        print("\n=== ZIP AI SOLVER ===")

        grid = self.get_grid()

        numbers = {v["num"]: k for k, v in grid.items() if v["num"]}
        max_num = max(numbers.keys())

        print("[NUMBERS]", numbers)

        path = self.solve(grid, numbers, max_num)

        if not path:
            print("[FAIL] No solution")
            return

        print("[SOLUTION]", path)

        self.execute(path)

    # MANUAL MODE
    # MANUAL MODE
    def play_with_solution(self, path, is_start_with_0 = False):
        print("\n=== MANUAL PLAY MODE ===")

        if not is_start_with_0:
            # if not start from 0 index
            path = [x-1 for x in path]

        print("[PATH]", path)

        if not path or len(path) < 2:
            print("[ERROR] Invalid path")
            return

        for i, idx in enumerate(path):
            try:
                print(f"[STEP {i+1}] Clicking {idx}")

                el = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f'[data-cell-idx="{idx}"]'
                )

                # self.driver.execute_script(
                #     "arguments[0].scrollIntoView({block: 'center'});",
                #     el
                # )

                
                ActionChains(self.driver)\
                    .move_to_element(el)\
                    .click()\
                    .perform()


                time.sleep(0.002)

            except Exception as e:
                print("[ERROR]", e)
                break

        print("[DONE] Path executed\n")


    

    # GRID PARSER
    def get_grid(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[data-testid^="cell-"]'
        )

        grid = {}

        for el in elements:
            try:
                idx = int(el.get_attribute("data-cell-idx"))

                label = el.get_attribute("aria-label")
                num = None
                if label and "Number" in label:
                    num = int(label.split(" ")[1])

                grid[idx] = {
                    "el": el,
                    "num": num
                }

            except:
                continue

        return grid

    # SOLVER
    def solve(self, grid, numbers, max_num):

        start = numbers[1]

        def get_neighbors(pos):
            r, c = divmod(pos, self.size)
            dirs = [(-1,0),(1,0),(0,-1),(0,1)]

            result = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    result.append(nr * self.size + nc)
            return result

        def dfs(pos, visited, current_num):

            # finished full grid
            if len(visited) == self.size * self.size:
                return visited

            neighbors = get_neighbors(pos)

            # prioritize next number
            neighbors.sort(
                key=lambda n: 0 if grid[n]["num"] == current_num + 1 else 1
            )

            for nxt in neighbors:

                if nxt in visited:
                    continue

                cell_num = grid[nxt]["num"]

                # enforce sequence
                if cell_num:
                    if cell_num != current_num + 1:
                        continue
                    next_num = current_num + 1
                else:
                    next_num = current_num

                # light pruning (safe)
                if cell_num is None:
                    dead = True
                    for nn in get_neighbors(nxt):
                        if nn not in visited:
                            dead = False
                            break
                    if dead:
                        continue

                result = dfs(nxt, visited + [nxt], next_num)

                if result:
                    return result

            return None

        return dfs(start, [start], 1)

    # EXECUTION
    def execute(self, path):
        print("\n[EXECUTE PATH]")

        for i, idx in enumerate(path):
            try:
                print(f"[STEP {i+1}] {idx}")

                el = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f'[data-cell-idx="{idx}"]'
                )

                ActionChains(self.driver)\
                    .move_to_element(el)\
                    .click()\
                    .perform()

                time.sleep(0.02)

            except Exception as e:
                print("[CLICK ERROR]", e)
                break
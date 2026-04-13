class BaseGame:
    def __init__(self, driver):
        self.driver = driver

    def play(self):
        raise NotImplementedError("Game must implement play() method")
    
    def safe_click(self, element):
        try:
            self.driver.execute_script(
                "arguments[0].click();", element
            )
        except:
            pass
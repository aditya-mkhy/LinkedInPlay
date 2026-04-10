from core.browser import create_browser

driver = create_browser()

driver.get("https://www.linkedin.com")

input("Press Enter to close...")
driver.quit()
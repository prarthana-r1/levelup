from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Test Case: Check if game loads
def test_game_load():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000")  # Update with your local Flask app URL
    time.sleep(2)

    assert "Game Title" in driver.title  # Change to your game’s title
    print("✅ Game loaded successfully!")

    driver.quit()

# Test Case: Simulate a user clicking start
def test_start_game():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000")  
    time.sleep(2)

    start_button = driver.find_element(By.ID, "start-button")  # Update with your button’s ID
    start_button.click()
    time.sleep(2)

    assert "Game Started" in driver.page_source  # Change to a unique indicator
    print("✅ Game started successfully!")

    driver.quit()

# Run Tests
if __name__ == "__main__":
    test_game_load()
    test_start_game()

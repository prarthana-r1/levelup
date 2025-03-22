from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Test Case: Check if game loads
def test_game_load():
    driver = setup_driver()
    driver.get("https://levelup-n5hr.onrender.com")  # Change if testing locally
    time.sleep(2)

    assert "Your Game Name" in driver.title  # Update with actual title
    print("✅ Game loaded successfully!")

    driver.quit()

# Test Case: Simulate a user clicking start
def test_start_game():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000")  
    time.sleep(2)

    try:
        start_button = driver.find_element(By.ID, "start-button")  # Ensure this ID is correct
        start_button.click()
        time.sleep(2)

        assert driver.find_element(By.ID, "game-container")  # Ensure this exists
        print("✅ Game started successfully!")

    except Exception as e:
        print("❌ Test failed:", str(e))

    driver.quit()

# Run Tests
if __name__ == "__main__":
    test_game_load()
    test_start_game()

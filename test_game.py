from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Determine URL (local or deployed)
LOCAL_URL = "http://127.0.0.1:5000"
DEPLOYED_URL ="https://your-app.onrender.com"
BASE_URL = os.getenv("TEST_URL", DEPLOYED_URL)  # Default to deployed version

# Setup WebDriver
def setup_driver():
    options = Options()
    #options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--no-sandbox")  # Required for running on servers
    options.add_argument("--disable-dev-shm-usage")  # Fixes memory issues
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Test Case: Check if game loads
def test_game_load():
    driver = setup_driver()
    driver.get(BASE_URL)
    
    # Wait for the title to appear
    #print(driver.title)
    WebDriverWait(driver, 10).until(EC.title_contains("LetsChiLL - Game Collection"))  # Update with actual title
    print("✅ Game loaded successfully!")

    driver.quit()

# Test Case: Simulate a user clicking start
def test_start_game():
    driver = setup_driver()
    driver.get(BASE_URL)
    
    try:
        # Wait for the start button to appear
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "start-button"))
        )
        start_button.click()

        # Wait for the game container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "game-container"))
        )
        
        print("✅ Game started successfully!")

    except Exception as e:
        print("❌ Test failed:", str(e))

    driver.quit()

# Run Tests
if __name__ == "__main__":
    test_game_load()
    test_start_game()

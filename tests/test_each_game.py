import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://levelupgames.onrender.com"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for CI/CD
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_game_functionality(driver):
    driver.get(BASE_URL)

    # Ensure page fully loads
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
    print("✅ Page fully loaded!")

    # Scroll down to trigger lazy loading
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

    # Locate game section
    try:
        games_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "games-container"))
        )
        print("✅ Found 'games-container' section in DOM!")
    except TimeoutException:
        print("❌ 'games-container' section not found!")
        driver.save_screenshot("error_games_container_not_found.png")
        raise AssertionError("❌ 'games-container' section not found!")

    # Locate game cards
    try:
        game_cards = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "game-card"))
        )
        print(f"✅ Found {len(game_cards)} game(s) in the section!")
    except TimeoutException:
        print("❌ No game cards found!")
        driver.save_screenshot("error_no_game_cards.png")
        raise AssertionError("❌ No game cards found!")

    # Click the first game
    game_cards[0].click()
    print("🎮 Clicking the first game card...")

    # Check if the new game page loads
    try:
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("✅ Game page loaded!")
    except TimeoutException:
        print("❌ Game page did not load after clicking!")
        driver.save_screenshot("error_game_page_not_loaded.png")
        raise AssertionError("❌ Game page did not load after clicking!")

    # Check for iframe (for embedded games)
    try:
        game_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        print("✅ Game iframe found!")
        driver.switch_to.frame(game_iframe)  # Switch to iframe
    except TimeoutException:
        print("⚠️ No iframe found, checking for canvas...")

    # Check for canvas (for HTML5 games)
    try:
        game_canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print("✅ Game canvas found!")
    except TimeoutException:
        print("❌ No iframe or canvas found! The game might not be working.")
        driver.save_screenshot("game_not_working.png")
        print(driver.page_source)  # Log page source for debugging
        raise AssertionError("❌ No iframe or canvas found! The game might not be working.")

    # Simulate a keypress to check interaction (SPACE key)
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.SPACE)
        print("✅ Sent SPACE key press to game!")
    except Exception as e:
        print(f"⚠️ Could not send keypress: {e}")

    time.sleep(3)  # Let the game react before closing

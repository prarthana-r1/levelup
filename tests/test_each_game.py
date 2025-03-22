import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

BASE_URL = "https://levelupgames.onrender.com"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # TEMPORARILY DISABLED for debugging
    options.add_argument("--window-size=1920,1080")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_each_game(driver):
    driver.get(BASE_URL + "#games")  # 🚀 Navigate directly

    try:
        # Wait for full page load
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("✅ Page fully loaded!")

        # Scroll down fully to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Save page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Ensure 'games' section is present
        games_section = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "games"))
        )
        print("🔎 Found 'games' section in DOM!")

        # Ensure 'games' section is visible
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "games"))
        )
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", games_section)
        print("✅ Games section is visible!")

        # Ensure game cards load
        game_cards = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "game-card"))
        )
        assert game_cards, "❌ No games found!"
        print(f"✅ Found {len(game_cards)} game(s) in the section!")

        # Store main window handle
        main_window = driver.current_window_handle

        for index, game_card in enumerate(game_cards):
            print(f"🔍 Testing game {index + 1}...")

            # Find "Play Now" button inside the game card
            play_button = game_card.find_element(By.CLASS_NAME, "game-card__button")
            game_url = play_button.get_attribute("onclick").split("location.href='")[1].split("'")[0]

            # Open game in a new tab
            driver.execute_script("window.open(arguments[0], '_blank');", game_url)
            driver.switch_to.window(driver.window_handles[-1])  # Switch to new tab

            # Wait for game page to load
            WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
            print(f"🎮 Game {index + 1} loaded successfully!")

            # Screenshot for debugging (optional)
            driver.save_screenshot(f"game_{index+1}.png")

            # Close the game tab and switch back to main window
            driver.close()
            driver.switch_to.window(main_window)

    except TimeoutException:
        driver.save_screenshot("test_each_game_error.png")
        raise AssertionError("❌ Games section did not load in time!")

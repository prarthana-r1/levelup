import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://levelupgames.onrender.com"

@pytest.mark.dependency(name="test_game_load")
def test_game_load(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.title_contains("LetsChiLL - Game Collection"))
    print("✅ Game loaded successfully!")

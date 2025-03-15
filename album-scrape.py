from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Remove Selenium detection
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# URL to scrape (main page with album list)
url = "https://www.albumoftheyear.org/ratings/user-highest-rated/all/"
driver.get(url)

# Randomized wait to avoid detection
time.sleep(random.uniform(5, 10))

# Find all album links
albums = driver.find_elements(By.CSS_SELECTOR, "a[itemprop='url']")
print(f"Found {len(albums)} album links.")

# Process first album only (for now)
if albums:
    album = albums[0]

    # Scroll and hover over album
    driver.execute_script("arguments[0].scrollIntoView();", album)
    time.sleep(random.uniform(3, 5))  # Simulate reading

    actions = ActionChains(driver)
    actions.move_to_element(album).perform()
    time.sleep(random.uniform(2, 4))  # Simulate hesitation

    # Click album link
    album_url = album.get_attribute('href')
    print(f"Navigating to album: {album_url}")
    driver.get(album_url)

    # **Manual CAPTCHA Handling**
    print("Solve the CAPTCHA manually, then press Enter in the terminal to continue...")
    input("Press Enter once you've solved the CAPTCHA: ")

    # **Wait for album page to fully load after CAPTCHA**
    time.sleep(random.uniform(7, 12))

    # Extract album details
    try:
        album_name = driver.find_element(By.CLASS_NAME, "albumTitle").text.strip()
        artist_name = driver.find_element(By.CLASS_NAME, "artistTitle").text.strip()
        critic_score = driver.find_element(By.CLASS_NAME, "scoreCritic").text.strip()
        user_score = driver.find_element(By.CLASS_NAME, "scoreUser").text.strip()

        print(f"Album: {album_name}")
        print(f"Artist: {artist_name}")
        print(f"Critic Score: {critic_score}")
        print(f"User Score: {user_score}")
    except Exception as e:
        print("Error scraping album details:", e)

    # Randomized wait before going back
    time.sleep(random.uniform(10, 15))

    # Instead of "back", reload the main page
    driver.get(url)
    time.sleep(random.uniform(10, 15))

# Close driver
driver.quit()

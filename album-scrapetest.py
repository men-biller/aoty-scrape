from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import random


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())

with open("album_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Album Name", "Artist", "Critic Score", "User Score"])

    for page_num in range(1, 5):
        driver = webdriver.Chrome(service=service, options=options)
        page_url = f"https://www.albumoftheyear.org/ratings/user-highest-rated/all/{page_num}/"
        driver.get(page_url)
        print(f"Saving HTML for page {page_num}: {page_url}")
        
        time.sleep(random.uniform(10, 20))  # wait to avoid CAPTCHA detection
        
        filename = f"albums{page_num}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        driver.quit()

for page_num in range(1, 5):
    filename = f"albums{page_num}.txt"
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    albums = soup.find_all("a", itemprop="url")
    
    for album in albums:
        album_url = "https://www.albumoftheyear.org" + album.get("href")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(album_url)
        print(f"Scraping album page: {album_url}")
        
        time.sleep(random.uniform(5, 10))  
        
        album_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        album_title = album_soup.select_one("h1.albumTitle span[itemprop='name']")
        album_title = album_title.text.strip() if album_title else "Unknown Album"

        artist_name = album_soup.select_one("span[itemprop='name'] a")
        artist_name = artist_name.text.strip() if artist_name else "Unknown Artist"

        critic_score = album_soup.select_one("span[itemprop='ratingValue']")
        critic_score = critic_score.text.strip() if critic_score else "No Critic Score"

        user_score = album_soup.select_one("div.albumUserScore a")
        user_score = user_score.text.strip() if user_score else "No User Score"

        with open("album_data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([album_title, artist_name, critic_score, user_score])
            print(f"Scraped: {album_title} by {artist_name} | Critic: {critic_score}, User: {user_score}")
        
        driver.quit()

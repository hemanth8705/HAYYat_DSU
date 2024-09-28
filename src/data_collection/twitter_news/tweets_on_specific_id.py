import json  # Import the JSON module
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import os
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from data_collection.twitter_news.twitter_details import get_details





# Function to save cookies to a file
def save_cookies(driver, filepath):
    with open(filepath, "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

# Function to load cookies from a file
def load_cookies(driver, filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)


def start_twitter_scraping_on_id(profile_username , limit = 5):
    
    # Set up Chrome options
    CHROMEDRIVER_PATH = 'data_collection\chromedriver.exe'

    # Set up Chrome options for headless mode
    options = Options()
    options.headless = True  # Uncomment if you want to run headlessly
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    user_name , password = get_details()
    # Cookie file path
    cookie_file = "twitter_cookies.pkl"

    # Open Twitter
    driver.get('https://x.com/login')
    time.sleep(5)

    # Check if cookies exist to avoid logging in every time
    if os.path.exists(cookie_file):
        load_cookies(driver, cookie_file)
        driver.refresh()  # Refresh to apply cookies and login
    else:
        # Login if no cookies are found
        username_field = driver.find_element(By.NAME, 'text')
        username_field.send_keys(user_name)  # Replace with your username
        username_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)  # Replace with your password
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Save cookies after successful login
        save_cookies(driver, cookie_file)

    # Step 1: Define the profile username
    profile_username = profile_username  # Replace with the desired username

    # Step 2: Navigate to the user's profile
    driver.get(f'https://x.com/{profile_username}')
    time.sleep(5)

    # Step 3: Collect the latest 3 tweet IDs by opening each tweet, saving the ID, and then returning to the profile
    tweet_ids = []
    

    for i in range(limit):  # Increase the range to collect enough valid tweets, ignore invalid ones
        # Find the latest tweet elements (articles)
        try:
            tweet = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]//a[contains(@href, "/status/")]')[i]
            
            # Open the tweet by clicking on it
            tweet.click()
            time.sleep(3)  # Wait for the tweet to load

            # Extract the tweet URL and get the tweet ID
            current_url = driver.current_url
            tweet_id = current_url.split('/')[-1]
            
            # Validate the tweet ID format (ensure it's a numerical ID, not something like 'analytics')
            if tweet_id.isdigit():
                tweet_ids.append(tweet_id)
                print(f"Tweet {len(tweet_ids)} ID: {tweet_id}")
            else:
                print(f"Skipped invalid tweet ID: {tweet_id}")

            # Navigate back to the user's profile
            driver.back()
              # Wait for the profile page to load

            # Stop after collecting 3 valid tweet IDs
            if len(tweet_ids) == 3:
                break
        except Exception as e:
            print(f"Error opening tweet: {e}")
        time.sleep(3)

    # Step 4: Now revisit each tweet URL and scrape comments
    all_comments = []

    for tweet_id in tweet_ids:
        # Construct the tweet URL using the stored tweet ID
        tweet_url = f'https://x.com/{profile_username}/status/{tweet_id}'
        print(f"Opening Tweet URL: {tweet_url}")
        driver.get(tweet_url)
        time.sleep(5)  # Adjust time as needed for loading the page

        # Scroll down to load all comments
        for _ in range(1):  # Adjust the number of scrolls as needed
            driver.execute_script("window.scrollTo(0, 100);")
            time.sleep(2)

        # Extract comments (and potentially replies)
        comments = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        tweet_comments = [[comment.text.strip()] for comment in comments]
        
        # print(f"Comments for Tweet {tweet_id}: {twee
        
        
        # Append tweet comments to the main list as a dictionary
        all_comments.append({
            "tweet_url": tweet_url,
            "comments": tweet_comments,
        })

    # Step 5: Save comments to JSON
    file_path = r"scraped_data/tweets_on_id.json"
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_comments, json_file, ensure_ascii=False, indent=4)

    # Close the browser
    driver.quit()

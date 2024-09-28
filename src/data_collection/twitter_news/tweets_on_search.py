import time
import os
import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
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

def start_twitter_scraping_on_search(query , limit = 5):               
    user_name , password = get_details()

    # Set up Chrome options for headless mode
    # options = Options()
    # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    # options.add_argument('--headless')  # Run in headless mode
    # options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    # options.add_argument('--no-sandbox')  # Bypass OS security model
    # options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    # options.add_argument('--window-size=1920x1080')  # Set a window size for headless mode

    # Initialize WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    CHROMEDRIVER_PATH = 'data_collection\chromedriver.exe'

    # Set up Chrome options for headless mode
    options = Options()
    options.headless = True  # Uncomment if you want to run headlessly
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)




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

    # Navigate to the search page (or desired profile)
    driver.get(f'https://x.com/search?q={query}&src=typed_query')
    print(f"twitter searching query {query}")
    time.sleep(5)

    # Scroll down to load tweets
    for _ in range(limit):
        driver.execute_script("window.scrollTo(0, 150);")
        time.sleep(3)

    # Extract tweets, their usernames, and their URLs by working within the tweet's parent 'article' element
    tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

    # Prepare a list to store tweet data
    tweet_data = []

    # Extract the tweet text, username, and URL for each tweet
    for tweet_element in tweet_elements:
        try:
            # Extract tweet text
            tweet_text_element = tweet_element.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
            tweet_text = tweet_text_element.text.strip()

            # Extract username
            username_element = tweet_element.find_element(By.XPATH, './/div[2]//div[1]//div[1]//span')
            username = username_element.text.strip()

            # Extract tweet URL
            tweet_url_element = tweet_element.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
            tweet_url = tweet_url_element.get_attribute('href')

            # Append tweet data to the list
            tweet_data.append({
                "username": username,
                "tweet": tweet_text,
                "url": tweet_url
            })

            print(f"Username: {username}, Tweet: {tweet_text}, URL: {tweet_url}")  # Debugging output

        except Exception as e:
            print(f"Error extracting tweet: {e}")
            continue

    # Step 3: Save the output to a JSON file
    output_filename = r"scraped_data/tweets_on_search.json"
    with open(output_filename, 'w', encoding='utf-8') as json_file: 
        json.dump(tweet_data, json_file, ensure_ascii=False, indent=4)

    print(f"Tweets saved to {output_filename}")

    # Close the browser
    driver.quit()

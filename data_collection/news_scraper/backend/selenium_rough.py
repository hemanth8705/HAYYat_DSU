from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  # New import for headless mode
import time
from bs4 import BeautifulSoup

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'chromedriver\chromedriver.exe'

# Function to perform Google search and scrape links
def scrape_google_news(query):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # To avoid memory issues in headless mode
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Initialize the WebDriver (Chrome)
    # driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    
    # Open Google search
    driver.get("https://www.google.com")
    
    # Perform search
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Allow the page to load

    # Use a set to store unique links
    links = set()
    start = time.time()
    while True:
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract all news-related links
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href and 'http' in href:
                links.add(href)  # Add to set to avoid duplicates
        
        # Sleep for 3 seconds to simulate delay and then scroll
        before_sleep = time.time()
        time.sleep(1)
        print(f"time slept {time.time() - before_sleep}")

        # Exit the loop if the scraping time exceeds 15 seconds
        if (time.time() - start) > 3:
            print("Search time exceeded 15 seconds. Exiting...")
            print(time.time() - start)
            break

    # Convert set of links to a list
    links = list(links)

    # Filter news links using specific keywords
    news_links = []
    def is_news_link(link):
        news_keywords = ["news", "times", "hindu", "economictimes", "ndtv", "indiatoday", "aajtak", "express", 
                         "livemint", "hindustantimes", "bbc", "aljazeera", "forbes", "theguardian", "reuters", "cnbc"]
        return any(keyword in link for keyword in news_keywords)

    for link in links:
        if is_news_link(link):
            news_links.append(link)

    print("Total news Links Found:", len(news_links))

    # Close the browser when finished
    driver.quit()

    return news_links


if __name__ == "__main__":
    q1 = "news about pm modi"
    scrape_google_news(q1)

    # You can explore the browser here before closing it manually
    # input("Press Enter to exit and close the browser...")
    # driver.quit()  # Uncomment this line if you want to close it programmatically

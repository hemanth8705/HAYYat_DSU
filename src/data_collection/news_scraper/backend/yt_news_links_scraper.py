from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  # New import for headless mode
import time
from bs4 import BeautifulSoup

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'chromedriver/chromedriver.exe'

# Function to perform YouTube search and scrape video links
def scrape_youtube(query):
    # Set up Chrome options for headless mode
    options = Options()
    options.headless = True  # Uncomment if you want to run headlessly
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open YouTube
    driver.get("https://www.youtube.com")
    
    # Perform search
    search_box = driver.find_element("name", "search_query")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Allow the page to load

    # Use a set to store unique links
    links = set()
    start = time.time()
    while True:
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract video links
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href and '/watch' in href:
                full_link = "https://www.youtube.com" + href
                links.add(full_link)  # Add to set to avoid duplicates
        
        # Scroll down to load more videos
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)  # Allow time for new content to load

        # Exit the loop if the scraping time exceeds 30 seconds
        if (time.time() - start) > 30:
            print("Search time exceeded 30 seconds. Exiting...")
            break

    # Convert set of links to a list
    video_links = list(links)

    print("Total video Links Found:", len(video_links))

    # Close the browser when finished
    driver.quit()

    return video_links

if __name__ == "__main__":
    q1 = "news about pm modi"
    video_links = scrape_youtube(q1)
    print(video_links)  # Print the found video links

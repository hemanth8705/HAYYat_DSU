import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_full_article(link):
    try:
        article_page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10, allow_redirects=True)
        article_page.raise_for_status()

        if article_page.url != link:
            # print(f"Redirected to {article_page.url}. This may require sign-in.")
            return None  # Return None for redirections

        article_soup = BeautifulSoup(article_page.content, 'html.parser')
        if "sign in" in article_soup.text.lower() or "captcha" in article_soup.text.lower():
            # print(f"Sign-in or CAPTCHA detected at {link}. Skipping article.")
            return None  # Return None for sign-in or CAPTCHA

        paragraphs = article_soup.find_all('p')
        full_text = " ".join([p.get_text() for p in paragraphs if len(p.get_text().strip()) > 20])

        if len(full_text.strip()) == 0:
            return None  # Return None for empty content

        return full_text
    except requests.exceptions.RequestException as e:
        # print(f"Error while fetching article: {e}")
        return None  # Return None for request errors
    except Exception as e:
        # print(f"General error: {e}")
        return None  # Return None for general errors

def bing_news_scraper(query, max_articles=7):
    news_data = []
    count = 0
    total_articles = 0
    offset = 0  # Starting point for pagination

    while count < max_articles:
        search_url = f"https://www.bing.com/news/search?q={query}&first={offset}"
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})

        if response.status_code != 200:
            # print(f"Failed to retrieve the news page, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('div', class_='t_s'):
            if count >= max_articles:
                break

            link_tag = item.find('a', class_='title')
            headline = link_tag.text.strip() if link_tag else "No headline"
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No link"

            if link != "No link":
                full_article = get_full_article(link)
                if full_article:  # Only append if full article is retrieved
                    news_data.append([headline, link, full_article])
                    count += 1  # Increment only for valid entries
                total_articles += 1

        # Increase the offset to fetch the next set of results
        offset += 10  # Each page typically contains 10 articles

    # Filter out any entries with empty full articles
    news_data = [entry for entry in news_data if entry[2] is not None]

    # Ensure we have a maximum of 70 valid entries
    if len(news_data) > max_articles:
        news_data = news_data[:max_articles]


    df = pd.DataFrame(news_data, columns=['Headline', 'Link', 'Full Article'])
    # df.to_csv(f'{query}.csv', index=False)
    print(f"out of {total_articles} scraped articels , {count} were found valid")
    return df



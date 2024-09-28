from flask import Flask, jsonify, request
from scraper import scrape_google_news

app = Flask(__name__)

# Store scraped links in memory for now (you can later use a database)
scraped_links = []

# Route to scrape news based on a query
@app.route('/scrape-news', methods=['GET', 'POST'])
def scrape_news():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is missing'}), 400

    # Scrape the news links for the provided query
    global scraped_links
    scraped_links = scrape_google_news(query)

    return jsonify({'status': 'Scraping started', 'links': scraped_links})

# Route to fetch the scraped links
@app.route('/get-links', methods=['GET', 'POST'])
def get_links():
    return jsonify({'links': scraped_links})

from flask import send_from_directory

# Route to serve the frontend files
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)


if __name__ == '__main__':
    app.run(debug=True)

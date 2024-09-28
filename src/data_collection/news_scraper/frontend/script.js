// Function to send a search query to the backend
function searchNews() {
    const query = document.getElementById('search-query').value;
    
    // Send a POST request to the Flask backend with the search query
    fetch('http://127.0.0.1:5000/scrape-news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Scraping started:', data);
        // Fetch and display the scraped links after a delay
        setTimeout(fetchLinks, 5000);  // Adjust delay as necessary
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to fetch and display saved links
function fetchLinks() {
    // Fetch the scraped links from the Flask backend
    fetch('http://127.0.0.1:5000/get-links')
    .then(response => response.json())
    .then(data => {
        const linksList = document.getElementById('saved-links');
        linksList.innerHTML = '';  // Clear any previous links
        
        // Display each link in the left pane
        data.links.forEach(link => {
            const listItem = document.createElement('li');
            const linkElement = document.createElement('a');
            linkElement.href = link;
            linkElement.textContent = link;
            linkElement.target = '_blank';  // Open link in new tab
            listItem.appendChild(linkElement);
            linksList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

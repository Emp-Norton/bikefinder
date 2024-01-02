import requests
from bs4 import BeautifulSoup

def craigslist_scraper(city, category, keyword):
    base_url = f"https://{city}.craigslist.org"
    search_url = f"{base_url}/search/{category}?query={keyword}"

    # Send a GET request to the Craigslist search page
    response = requests.get(search_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure
        for listing in soup.find_all('li', class_='result-row'):
            title = listing.find('a', class_='result-title').text
            link = listing.find('a', class_='result-title')['href']
            price = listing.find('span', class_='result-price').text.strip()

            # Print or process the information as needed
            print(f"Title: {title}\nPrice: {price}\nLink: {base_url}{link}\n")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Example usage
craigslist_scraper("example-city", "forsale", "your-keyword")


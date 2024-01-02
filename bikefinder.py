import requests, time

from bs4 import BeautifulSoup
from selenium import webdriver


def set_custom_headers(driver, headers):
    for key, value in headers.items():
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": value})

def setup_browser()
    browser = webdriver.Chrome('chromedriver')
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--enable-javascript')
    options.add_argument("--headless")

    #TODO Load headers and set them using the helper functions, also rearrange this to be more logical and clear
    return browser

def load_headers(headerfile='./requestinfo.data'):
    header_objects = {"User-Agent": None, "Accept": None}

    with open(headerfile, 'r') as f:
        data = f.readlines()

    for i in range(len(data)):
        item = data[i]
        parts = item.split("=")
        if 'user_agent' in item:
            header_objects['User-Agent'] = parts[1].strip()
        if 'accept' in item:
            header_objects['Accept'] = parts[1].strip()

    return header_objects

def craigslist_scraper(city, category, keyword):
    base_url = f"https://{city}.craigslist.org"
    search_url = f"{base_url}/search/{category}?query={keyword}"
    headers = load_headers()

    # Send a GET request to the Craigslist search page
    print(f"Sending request to CL with headers: {headers}, using URL: {search_url}")
    response = requests.get(search_url, headers=headers)
    print(f"Received: {response}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # Extract information based on the HTML structure
        for listing in soup.find_all('li', class_='result-row'):
            title = listing.find('a', class_='result-title').text
            link = listing.find('a', class_='result-title')['href']
            price = listing.find('span', class_='result-price').text.strip()

            # Print or process the information as needed
            print(f"Title: {title}\nPrice: {price}\nLink: {base_url}{link}\n")
        return soup
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return response

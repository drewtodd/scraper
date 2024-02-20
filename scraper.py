import requests
from bs4 import BeautifulSoup
from collections import Counter

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags in the document
    links = soup.find_all('a', href=True)

    # Filter links that point to 'cti.com'
    filtered_links = [link for link in links if 'cti.com' in link['href']]

    # Extract and clean link texts
    link_texts = [link.get_text(strip=True).lower() for link in filtered_links if link.get_text(strip=True)]

    # Count occurrences of each term
    term_counts = Counter(link_texts)

    # Print term counts
    for term, count in term_counts.items():
        print(f"Term: '{term}', Count: {count}")

# Replace the URL with the webpage you want to scrape
scrape_website('https://avnation.tv')

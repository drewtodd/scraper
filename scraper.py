import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
import random
import time

def is_internal_url(url, base_domain):
    parsed_url = urlparse(url)
    return parsed_url.netloc == '' or parsed_url.netloc.endswith(base_domain)

def scrape_website(url, base_domain, visited_urls, term_counts, output_file, verbose):
    if url in visited_urls:
        return
    visited_urls.add(url)

    if verbose:
        print(f"Processing {url}")

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Only consider links within the div with class 'td-main-content-wrap'
        main_content_div = soup.find('div', class_='td-main-content-wrap')
        if main_content_div:
            links = main_content_div.find_all('a', href=True)
        else:
            links = []
            if verbose:
                print(f"No main content div found in {url}")

        for link in links:
            href = link['href']
            full_url = urljoin(url, href)

            if 'cti.com' in href:
                link_text = link.get_text(strip=True).lower()
                if link_text:
                    term_counts[link_text] += 1
                    with open(output_file, 'a') as file:
                        file.write(f"Term: '{link_text}', Count: {term_counts[link_text]}\n")
                    if verbose:
                        print(f"Found and logged link: {href} with text '{link_text}'")

            if is_internal_url(href, base_domain):
                time.sleep(random.randint(0, 0))  # Random delay between 3 and 10 seconds
                if verbose:
                    print(f"Following internal link: {full_url}")
                scrape_website(full_url, base_domain, visited_urls, term_counts, output_file, verbose)
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")

def main(start_url, output_file, verbose=False):
    base_domain = 'avnation.tv'
    visited_urls = set()
    term_counts = Counter()

    # Clear the output file at the beginning of the run
    open(output_file, 'w').close()

    scrape_website(start_url, base_domain, visited_urls, term_counts, output_file, verbose)

# Example usage
main('https://www.avnation.tv/casestudies/', 'output.txt', verbose=True)

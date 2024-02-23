import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
import random
import time

def is_internal_url(url, base_domain):
    parsed_url = urlparse(url)
    return parsed_url.netloc == '' or parsed_url.netloc.endswith(base_domain)

def scrape_website(url, base_domain, visited_urls, term_counts, output_file, log_file, mode, verbose):
    if url in visited_urls:
        return
    visited_urls.add(url)

    if verbose:
        print(f"Processing {url}")

    # Define custom headers with a User-Agent of your choice
    headers = {
        'User-Agent': 'Your User-Agent String Here',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Include the custom headers in the request
        response = requests.get(url, headers=headers)
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
            link_text = link.get_text(strip=True)

            if 'cti.com' in href:
                if mode == "log":
                    with open(log_file, 'a') as file:
                        file.write(f"Link Term: '{link_text}', Current URL: {url}, CTI Link: {href}\n")
                    if verbose:
                        print(f"Logged CTI link: {href} with term '{link_text}' from {url}")
                else:  # Summary mode
                    link_text_lower = link_text.lower()
                    if link_text_lower:
                        term_counts[link_text_lower] += 1
                        with open(output_file, 'a') as file:
                            file.write(f"Term: '{link_text_lower}', Count: {term_counts[link_text_lower]}\n")

            if is_internal_url(href, base_domain):
                time.sleep(random.randint(1, 3))  # Random delay between 1 and 3 seconds
                if verbose:
                    print(f"Following internal link: {full_url}")
                scrape_website(full_url, base_domain, visited_urls, term_counts, output_file, log_file, mode, verbose)
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")

def main(start_url, output_file, log_file, mode="summary", verbose=False):
    base_domain = 'avnation.tv'
    visited_urls = set()
    term_counts = Counter()

    if mode == "summary":
        # Clear the output file at the beginning of the run
        open(output_file, 'w').close()
    else:  # Log mode
        open(log_file, 'w').close()

    scrape_website(start_url, base_domain, visited_urls, term_counts, output_file, log_file, mode, verbose)

# Example usage
main('https://www.avnation.tv/casestudies/', 'output_summary.txt', 'output_log.txt', mode="log", verbose=True)

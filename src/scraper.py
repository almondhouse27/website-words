import robots
import logging as log
import requests
import time
from bs4 import BeautifulSoup
from logparser import executeLogParser
from utils import \
    setupProjectStructure, \
    readDataInput, \
    writeWordData, \
    writeSiteData, \
    sortDataOutput

HEADERS = {'User-Agent': 'Mozilla/5.0'}
DIRECTORIES = ['data', 'data/input', 'data/output']
LOG_FILE = 'logs/scraper.log'
LOG_OUTPUT = 'data/output'
INPUT_FILE = 'data/input/url-list.csv'
BACKUP_FILE = 'backup/url-list.csv'

log.basicConfig(
        filename=LOG_FILE,
        level=log.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
)

###--------------------------------->>>>>>>
"""
"""
def scrapeWebsite(url):

    try:
        # send an HTTP request to the provided URL with specified headers
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        log.info(f"Successfully fetched {url}")

        # parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'lxml')

        # extract and process the text content (word-data)
        # store word-data in word_count dictionary
        text_content = soup.get_text(separator=' ')
        word_count = {}
        for word in text_content.split():
            word = word.lower().strip('.,!?')
            word_count[word] = word_count.get(word, 0) + 1
        log.info(f"Word count completed for {url}")

        # extract site details (site-data)
        image_count = len(soup.find_all('img'))
        link_count = len(soup.find_all('a'))
        form_count = len(soup.find_all('form'))
        css_count = len(soup.find_all('link', rel='stylesheet'))
        js_count = len(soup.find_all('script', src=True))
        '''placeholder for certificate information'''
        cert_info = 'N/A'
        host_info = 'N/A'
        title = soup.find('meta', attrs={'name': 'title'}).get('content', '').strip() \
            if soup.find('meta', attrs={'name': 'title'}) else 'N/A'
        description = soup.find('meta', attrs={'name': 'description'})['content'] \
            if soup.find('meta', attrs={'name': 'description'}) else 'N/A'
        
        # store site-data in site_details dictionary
        site_details = {
            'images': image_count,
            'links': link_count,
            'forms': form_count,
            'stylesheets': css_count,
            'scripts': js_count,
            'cert': cert_info,
            'host': host_info,
            'title': title,
            'description': description,
        }

        # return a dictionary of dictionaries
        return {
            'words': word_count,
            'site': site_details
        }
    
    # handle and log request errors if any
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching {url}: {e}")
        return None
    
###--------------------------------->>>>>>>
"""
"""
def executeWebsiteWords():
    try:
        setupProjectStructure(INPUT_FILE, BACKUP_FILE, DIRECTORIES)

        urls_to_scrape = readDataInput()
        all_word_data = {}
        all_site_data = {}

        for institution, url in urls_to_scrape.items():
            disallowed_paths = robots.checkPermissions(url)

            if any(disallowed_path in url for disallowed_path in disallowed_paths):
                log.info(f"Skipping {url} due to disallowed path.")
                continue

            scraped_data = scrapeWebsite(url)

            if scraped_data:
                all_word_data[institution] = scraped_data['words']
                all_site_data[institution] = scraped_data['site']

        writeWordData(all_word_data)
        writeSiteData(all_site_data)
        sortDataOutput(
            'data/output/word-data-*.csv', 
            'data/output/site-data-*.csv'
        )

        log.info("[============================================] SUCCESS")

        executeLogParser(LOG_FILE, LOG_OUTPUT)
        # display success message
    
    except Exception as e:
        log.error(f"An error occurred during execution: {e}")

###--------------------------------->>>>>>>
"""
"""
if __name__ == "__main__":

    executeWebsiteWords()
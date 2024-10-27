from utils import setupProjectStructure, \
                  readDataInput, \
                  writeWordData, \
                  writeSiteData, \
                  sortDataOutput
from bs4 import BeautifulSoup
import logging
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}
DIRECTORIES = ['data', 'data/input', 'data/output']
LOG_FILE = 'logs/scraper.log'
INPUT_FILE = 'data/input/url-list.csv'
BACKUP_FILE = 'backup/url-list.csv'

logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
)

###--------------------------------->>>>>>>
"""
"""
def scrapeWebsite(url):

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        logging.info(f"Successfully fetched {url}")

        soup = BeautifulSoup(response.text, 'lxml')

        # data for word-data-timestamp.csv
        text_content = soup.get_text(separator=' ')
        word_count = {}
        for word in text_content.split():
            word = word.lower().strip('.,!?')
            word_count[word] = word_count.get(word, 0) + 1
        logging.info(f"Word count completed for {url}")

        # data for site-data-timestamp.csv
        image_count = len(soup.find_all('img'))
        link_count = len(soup.find_all('a'))
        js_true = any(script for script in soup.find_all('script'))
            # placeholder for certificate information
        cert_info = 'N/A'
        host_info = 'N/A'

        site_details = {
            'images': image_count,
            'links': link_count,
            'js': js_true,
            'cert': cert_info,
            'host': host_info
        }

        return {
            'words': word_count,
            'site': site_details
        }
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")

        return None

###--------------------------------->>>>>>>
"""
"""
if __name__ == "__main__":

    try:
        setupProjectStructure(INPUT_FILE, BACKUP_FILE, DIRECTORIES)

        urls_to_scrape = readDataInput()
        all_word_data = {}
        all_site_data = {}

        for institution, url in urls_to_scrape.items():
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

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
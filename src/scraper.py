from utils import setupProjectStructure, \
                  readDataInput, \
                  writeDataOutput
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
        text_content = soup.get_text(separator=' ')
        word_count = {}

        for word in text_content.split():
            word = word.lower().strip('.,!?')
            word_count[word] = word_count.get(word, 0) + 1
        logging.info(f"Word count completed for {url}")

        return word_count
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")

        return None

###--------------------------------->>>>>>>
"""
"""
if __name__ == "__main__":

    setupProjectStructure(INPUT_FILE, BACKUP_FILE, DIRECTORIES)

    urls_to_scrape = readDataInput()
    all_word_data = {}

    for institution, url in urls_to_scrape.items():
        word_data = scrapeWebsite(url)

        if word_data:
            all_word_data[institution] = word_data

    writeDataOutput(all_word_data)
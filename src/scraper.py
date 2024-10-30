import logging as log
import requests
import robots
from bs4 import BeautifulSoup
from diagnostics import Diagnostics
from logparser import executeLogParser
       
from utility import \
    setupProjectStructure, \
    readDataInput, \
    writeWordData, \
    writeSiteData, \
    sortDataOutput

HEADERS = {'User-Agent': 'Mozilla/5.0'}
DIRECTORIES = ['data', 'data/input', 'data/output']
LOG_OUTPUT = 'data/output'
LOG_FILE = 'logs/scraper.log'
INPUT_FILE = 'data/input/url-list.csv'
BACKUP_FILE = 'backup/url-list.csv'

log.basicConfig(
        filename=LOG_FILE,
        level=log.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
)

###--------------------------------->>>>>>>
#
def scrapeWebsite(url):

    try:
        # send an HTTP request to the provided URL with specified headers
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        log.info(f"Successfully fetched {url}")

        # parse the HTML content response
        soup = BeautifulSoup(response.text, 'lxml')

        # extract and process the text content (for -> word-data.csv)
        # store text content data in word_count dictionary
        text_content = soup.get_text(separator=' ')
        word_count = {}
        for word in text_content.split():
            word = word.lower().strip('.,!?')
            word_count[word] = word_count.get(word, 0) + 1
        log.info(f"Word count completed for {url}")

        # extract site details (for -> site-data.csv)
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
        
        # store site details and analytics in site_details dictionary
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
#
def executeWebsiteWords():

    try:
        # installs project dependencies, ensures data directory and its contents exists
        setupProjectStructure(LOG_FILE, INPUT_FILE, BACKUP_FILE, DIRECTORIES)

        log.info("[============================================] EXECUTING")

        # reads URLs from data/input/url-list.csv 
        urls_to_scrape = readDataInput()
        all_word_data = {}
        all_site_data = {}

        # reads site's robots.txt file and returns a disallowed paths list
        for institution, url in urls_to_scrape.items():
            disallowed_paths = robots.checkPermissions(url)

            # uses 'continue' to loop-skip scrapeWebsite() according to site's robots.txt file permissions
            if any(disallowed_path in url for disallowed_path in disallowed_paths):
                log.info(f"Skipping {url} due to disallowed path.")
                continue

            # takes in a URL, sends a request, parses and assembles the response into appropriate data dictionary
            scraped_data = scrapeWebsite(url)

            # splits scraped_data dictionary of dictionaries into two seperate dictionaries for writing output files
            if scraped_data:
                all_word_data[institution] = scraped_data['words']
                all_site_data[institution] = scraped_data['site']

        log.info("[============================================] WRITING")

        # writes word-data.csv and site-data.csv data output files
        writeWordData(all_word_data)
        writeSiteData(all_site_data)
        sortDataOutput(
            'data/output/*-word-data.csv', 
            'data/output/*-site-data.csv'
        )

        log.info("[============================================] TERMINATING")

        # converts logs/scraper.log to log-data.csv data output file
        executeLogParser(LOG_FILE, LOG_OUTPUT)
    
    except Exception as e:
        log.error("[============================================] FAILURE")
        log.error(f"An error occurred during execution: {e}")


###--------------------------------->>>>>>>
"""
APPLICATION:    Website Words
DEVELOPED BY:   David Blessent
REPOSITORY:     github.com/almondhouse27/website-words
COMMAND:        
PRODUCES:       produces timestamped json file and csv files in data/output/
                word-data.csv, site-data.csv, log-data.csv, diagnostic-summary.json

PURPOSE:        Website Words is a web scraper that processes a list of URLs from data/input/url-list.csv,
                sending HTTP requests and parsing the HTML responses to generate four timestamped files
                in the data/output/ directory. 
                
                Its primary goal is to produce word-data.csv, which lists every word found in the URLs' 
                HTML response along with its frequency.

                In addition, Website Words generates:
                  * site-data.csv
                        includes structural details about the website (e.g., number of images,
                        institution's state of operation).
                  * log-data.csv
                        contains the runtime log information parsed into CSV format as the 
                        final step of the executeWebsiteWords() script.
                  *  diagnostic-summary.json
                        provides runtime analytics, including duration, file sizes, request outcomes,
                        log level data, and descriptive statistics of the word-data.csv dataset.
"""
if __name__ == "__main__":
    runtime = Diagnostics()
    runtime.start()
    executeWebsiteWords()
    runtime.end()
    runtime.summary()
    
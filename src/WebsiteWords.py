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
import time
import logging as log
import robots
from diagnostics import Diagnostics
from scraper import scrapeWebsite
from logparser import executeLogParser     
from utility import \
    setupProjectStructure, \
    readDataInput, \
    writeWordData, \
    writeSiteData, \
    sortDataOutput

HEADERS = {'User-Agent': 'Mozilla/5.0'}
ROBOT_RETRY = 3
DIRECTORIES = ['data', 'data/input', 'data/output']
LOG_OUTPUT = 'data/output'
LOG_FILE = 'logs/scraper.log'
INPUT_FILE = 'data/input/url-list.csv'


log.basicConfig(
        filename=LOG_FILE,
        level=log.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
)

###--------------------------------->>>>>>>
#
def executeWebsiteWords():

    try:
        # installs project dependencies, ensures data directory and its contents exists
        setupProjectStructure(LOG_FILE)

        # reads URLs from data/input/url-list.csv 
        urls_to_scrape = readDataInput()
        all_word_data = {}
        all_site_data = {}

        # reads site's robots.txt file and returns a disallowed paths list
        for website, details in urls_to_scrape.items():
            log.info(f"Details for website {website}: {details}")
            institution = details['Institution']
            category = details['Category']
            state = details['State']
            city = details['City']
            disallowed_paths = robots.checkPermissions(website, ROBOT_RETRY)

            # uses 'continue' to loop-skip scrapeWebsite() according to site's robots.txt file permissions
            if any(disallowed_path in website for disallowed_path in disallowed_paths):
                log.info(f'Skipping {website} due to disallowed path.')
                #print(f'-Skipping {website} due to disallowed path.')
                continue

            # takes in a URL, sends a request, parses and assembles the response into appropriate data dictionary
            #scraped_data = scrapeWebsite(website, HEADERS)
            try:
                scraped_data = scrapeWebsite(website, HEADERS)
            except Exception as e:
                log.error(f"Error scraping {website}: {e}")
                #print(f"Error scraping {website}: {e}")
                continue
            
            # splits scraped_data dictionary of dictionaries into two seperate dictionaries for writing output files
            if scraped_data:
                all_word_data[website] = scraped_data['words']
                all_site_data[website] = {
                    'Category': category,
                    'State': state,
                    'City': city,
                    'Institution': institution,
                    **scraped_data['site']
                }

            # rate limiting
            time.sleep(.1) 

        # writes word-data.csv and site-data.csv data output files
        writeWordData(all_word_data)
        writeSiteData(all_site_data)
        sortDataOutput(
            'data/output/*-word-data.csv', 
            'data/output/*-site-data.csv'
        )

        # converts logs/scraper.log to log-data.csv data output file
        executeLogParser(LOG_FILE, LOG_OUTPUT)
    
    except Exception as e:
        log.error(f'An error occurred during execution: {e}')
        #print(f'An error occurred during execution: {e}')


###--------------------------------->>>>>>>
#
if __name__ == "__main__":
    runtime = Diagnostics()
    runtime.start()
    executeWebsiteWords()
    runtime.end()
    runtime.summary()
    
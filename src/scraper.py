import logging as log
import requests
from bs4 import BeautifulSoup

###--------------------------------->>>>>>>
#
def scrapeWebsite(website, HEADERS):

    try:
        # send an HTTP request to the provided URL with specified headers
        log.info(f'\tSending HTTP request to {website}')
        print(f'\tSending HTTP request to {website}')
        
        response = requests.get(website, headers=HEADERS)
        response.raise_for_status()
        
        log.info(f'Successfully fetched {website}')

        # parse the HTML content response
        soup = BeautifulSoup(response.text, 'lxml')

        # extract and process the text content (for -> word-data.csv)
        # store text content data in word_count dictionary
        text_content = soup.get_text(separator=' ')
        word_count = {}
        for word in text_content.split():
            word = word.lower().strip('.,!?')
            word_count[word] = word_count.get(word, 0) + 1
        log.info(f'Word count completed for {website}')

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
        log.error(f'Error fetching {website}: {e}')
        return None
from datetime import datetime
import csv
import glob as bolg
import logging as log
import os
import pandas as pd
import shutil
import subprocess

###--------------------------------->>>>>>>
# verify data directories and input file exist, create data directories and copy backup input if !exists
def setupProjectStructure(LOG_FILE):
    log_file = LOG_FILE

    try:
        with open(log_file, 'w'):
            pass

        log.info(f'U- Refreshed contents of log file for this runtime: {log_file}')
        print((f'U- Refreshed contents of log file for this runtime: {log_file}'))

    except Exception as e:
        log.error(f'U- Failed to clear log file: {e}')
        print(f'U- Failed to clear log file: {e}')

    # try:
    #     with open(os.devnull, 'w') as devnull:
    #         subprocess.check_call([
    #                 os.sys.executable,
    #                 '-m', 'pip', 'install', '-r', 'requirements.txt'],
    #                 stdout=devnull,
    #                 stderr=devnull
    #         )
    try:
        result = subprocess.run(
            [os.sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        if result.stdout:
            log.info(f'U- All requirements are met, for details check: logs/scraper.log \n{result.stdout}')
            print('All requirements are met, for details check: logs/scraper.log')

        if result.stderr:
            log.warning(f'U- Warning/Error during installation, check scraper.log for details: \n{result.stderr}')
            print('Warning/Error during installation, for details check: logs/scraper.log ')
            
    except subprocess.CalledProcessError as e:
        log.error(f'U- Error installing requirements: {e}')
        print('Error installing requirements, for details check: logs/scraper.log')
        
    except Exception as e:
        log.error(f'U- Unexpected error during installation: {e}')
        print('Unexpected error during installation, for details check: logs/scraper.log')


###--------------------------------->>>>>>>
# read URLs from CSV input file
def readDataInput(filename='data/input/url-list.csv'):
    url_list = {}

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)

            # for row in reader:
            #     url_list[row['Institution']] = row['Website']

            for row in reader:
                ##log.info(f"Row data: {row}")
                url_list[row['Website']] = {
                    'Category': row['Category'],
                    'State': row['State'],
                    'City': row['City'],
                    'Institution': row['Institution']
                }

        log.info(f'U- URLs loaded from `{filename}`')
        print(f'U- URLs loaded from `{filename}`')
        
    except Exception as e:
        log.error(f'U- Error loading URLs from `{filename}`: {e}')
        print((f'U- Error loading URLs from `{filename}`: {e}'))

    return url_list


###--------------------------------->>>>>>>
# write word count data to CSV file
def writeWordData(data, filename='data/output/word-data.csv'):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    base, ext = os.path.splitext(os.path.basename(filename))
    directory = os.path.dirname(filename)
    filename = f"{directory}/{timestamp}-{base}{ext}"

    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Website',
                'Word',
                'Count'
            ])

            for website, word_data in data.items():
                for word, count in word_data.items():
                    writer.writerow([
                        website,
                        word,
                        count
                    ])

        log.info(f'U- Word-data saved to `{filename}`')
        print(f'U- Word-data saved to `{filename}`')
    
    except Exception as e:
        log.error(f'U- Error saving word-data to `{filename}`: {e}')
        print(f'U- Error saving word-data to `{filename}`: {e}')
        

###--------------------------------->>>>>>>
# write site details data to CSV file
def writeSiteData(data, filename='data/output/site-data.csv'):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    base, ext = os.path.splitext(os.path.basename(filename))
    directory = os.path.dirname(filename)
    filename = f"{directory}/{timestamp}-{base}{ext}"

    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Website',
                'Institution',
                'Category',
                'State',
                'City',
                'ImageCount',
                'LinkCount',
                'FormCount',
                'StylesheetCount',
                'ScriptCount',
                'CertificateInfo',
                'HostInfo',
                'Title',
                'Description'
            ])

            for website, site_data in data.items():
                writer.writerow([
                    website,
                    site_data['Institution'],
                    site_data['Category'],
                    site_data['State'],
                    site_data['City'],
                    site_data['images'],
                    site_data['links'],
                    site_data['forms'],
                    site_data['stylesheets'],
                    site_data['scripts'],
                    site_data['cert'],
                    site_data['host'],
                    site_data['title'],
                    site_data['description'],
                ])

        log.info(f'U- Site-data saved to `{filename}`')
        print(f'U- Site-data saved to `{filename}`')

    except Exception as e:
        log.error(f'U- Error saving site-data to `{filename}`: {e}')
        print(f'U- Error saving site-data to `{filename}`: {e}')


###--------------------------------->>>>>>>
# sorts the datafiles after writing

def sortDataOutput(word_data_pattern, site_data_pattern):
    word_data_files = bolg.glob(word_data_pattern)
    latest_word_file = max(word_data_files, key=os.path.getctime) if word_data_files else None

    site_data_files = bolg.glob(site_data_pattern)
    latest_site_file = max(site_data_files, key=os.path.getctime) if site_data_files else None

    if latest_word_file:
        word_data = pd.read_csv(latest_word_file)
        sorted_word_data = word_data.sort_values(by=['Website', 'Word'])
        sorted_word_data.to_csv(latest_word_file, index=False)
        log.info(f'U- Sorted word-data saved to `{latest_word_file}`')
        print(f'U- Sorted word-data saved to `{latest_word_file}`')

    if latest_site_file:
        site_data = pd.read_csv(latest_site_file)
        sorted_site_data = site_data.sort_values(by=['Website'])
        sorted_site_data.to_csv(latest_site_file, index=False)
        log.info(f'U- Sorted site-data saved to `{latest_site_file}`')
        print(f'U- Sorted site-data saved to `{latest_site_file}`')
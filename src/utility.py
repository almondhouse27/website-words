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
def setupProjectStructure(LOG_FILE, INPUT_FILE, BACKUP_FILE, DIRECTORIES):

    log_file = LOG_FILE

    try:
        with open(log_file, 'w'):
            pass
        log.info("[============================================] INITIALIZING")
        log.info(f"Cleared contents of log file: {log_file}")

    except Exception as e:
        print(f"Failed to clear log file: {e}")

    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        log.info("All requirements installed successfully.")

    except subprocess.CalledProcessError as e:
        log.error(f"Error installing requirements: {e}")
        
    except Exception as e:
        log.error(f"Unexpected error during installation: {e}")

    if not os.path.exists(BACKUP_FILE):
        log.error(f"Backup file `{BACKUP_FILE}` is missing. Please clone a fresh copy of `almondhousepublishing27/website-words`.")

    for dir in DIRECTORIES:

        if not os.path.exists(dir):
            os.makedirs(dir)
            log.info(f"Created directory: {dir}")

    if not os.path.exists(INPUT_FILE):
        shutil.copy(BACKUP_FILE, INPUT_FILE)
        log.info(f"Copied `{BACKUP_FILE}` to `{INPUT_FILE}`")

    else:
        log.info(f"Backup file `{BACKUP_FILE}` not required.")


###--------------------------------->>>>>>>
# read URLs from CSV input file
def readDataInput(filename='data/input/url-list.csv'):

    url_list = {}

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                url_list[row['Institution']] = row['Website']

        log.info(f"URLs loaded from `{filename}`")
        
    except Exception as e:
        log.error(f"Error loading URLs from `{filename}`: {e}")

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
                'Institution',
                'Word',
                'Count'
            ])

            for institution, word_data in data.items():
                for word, count in word_data.items():
                    writer.writerow([
                        institution,
                        word,
                        count
                    ])

        
        log.info(f"Word-data saved to `{filename}`")
    
    except Exception as e:
        log.error(f"Error saving word-data to `{filename}`: {e}")
        

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
                'Institution',
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

            for institution, site_data in data.items():
                writer.writerow([
                    institution,
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

        log.info(f"Site-data saved to `{filename}`")

    except Exception as e:
        log.error(f"Error saving site-data to `{filename}`: {e}")


###--------------------------------->>>>>>>
# sorts the datafiles after writing

def sortDataOutput(word_data_pattern, site_data_pattern):

    word_data_files = bolg.glob(word_data_pattern)
    latest_word_file = max(word_data_files, key=os.path.getctime) if word_data_files else None

    site_data_files = bolg.glob(site_data_pattern)
    latest_site_file = max(site_data_files, key=os.path.getctime) if site_data_files else None

    if latest_word_file:
        word_data = pd.read_csv(latest_word_file)
        sorted_word_data = word_data.sort_values(by=['Institution', 'Word'])
        sorted_word_data.to_csv(latest_word_file, index=False)
        log.info(f"Sorted word-data saved to `{latest_word_file}`")

    if latest_site_file:
        site_data = pd.read_csv(latest_site_file)
        sorted_site_data = site_data.sort_values(by=['Institution'])
        sorted_site_data.to_csv(latest_site_file, index=False)
        log.info(f"Sorted site-data saved to `{latest_site_file}`")
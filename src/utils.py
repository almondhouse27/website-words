from datetime import datetime
import csv
import logging
import os
import shutil
import subprocess

###--------------------------------->>>>>>>
# verify directories and input file exist
def setupProjectStructure(INPUT_FILE, BACKUP_FILE, DIRECTORIES):

    try:
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logging.info("All requirements installed successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing requirements: {e}")

    except Exception as e:
        logging.error(f"Unexpected error during installation: {e}")

    if not os.path.exists(BACKUP_FILE):
        logging.error(f"Backup file `{BACKUP_FILE}` is missing. Please clone a fresh copy of `almondhousepublishing27/website-words`.")

    for dir in DIRECTORIES:

        if not os.path.exists(dir):
            os.makedirs(dir)
            logging.info(f"Created directory: {dir}")

    if not os.path.exists(INPUT_FILE):
        shutil.copy(BACKUP_FILE, INPUT_FILE)
        logging.info(f"Copied `{BACKUP_FILE}` to `{INPUT_FILE}`")

    else:
        logging.info(f"Backup file `{BACKUP_FILE}` not required.")

###--------------------------------->>>>>>>
# read URLs from CSV file
def readDataInput(filename='data/input/url-list.csv'):

    url_list = {}

    try:

        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                url_list[row['Institution']] = row['Website']

        logging.info(f"URLs loaded from `{filename}`")
        
    except Exception as e:
        logging.error(f"Error loading URLs from `{filename}`: {e}")

    return url_list

###--------------------------------->>>>>>>
# write word count data to CSV file
def writeDataOutput(data, filename='data/output/word-data.csv'):

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    base, ext = os.path.splitext(filename)
    filename = f"{base}-{timestamp}{ext}"

    try:

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Institution', 'Word', 'Count'])

            for institution, word_data in data.items():

                for word, count in word_data.items():
                    writer.writerow([institution, word, count])

        logging.info(f"Data saved to `{filename}`")

        if os.path.exists(filename):
            logging.info(f"File `{filename}` was successfully created.")

        else:
            logging.error(f"File `{filename}` was NOT created.")
    
    except Exception as e:
        logging.error(f"Error saving data to `{filename}`: {e}")

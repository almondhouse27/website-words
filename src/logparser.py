import csv
from datetime import datetime
import os

###--------------------------------->>>>>>>
# script for converting runtime log data in logs/scraper.log to a timestamped data output file
# produces: data/output/{timestamp}-log-data.csv
def executeLogParser(LOG_FILE, LOG_OUTPUT):
    log_lines = readScraperLog(LOG_FILE)
    log_data = parseScraperLog(log_lines)
    logToCsv(log_data, LOG_OUTPUT)
    
    
###--------------------------------->>>>>>>
# reads the contents of the scraper.log file and returns the lines
def readScraperLog(LOG_FILE):

    with open(LOG_FILE, 'r') as file:
        return file.readlines()
    

###--------------------------------->>>>>>>
# parses log lines into structured data with timestamps, log levels, and messages
def parseScraperLog(log_lines):
    log_data = []

    for line in log_lines:
        parts = line.split(' - ')

        if len(parts) >= 3:
            timestamp = parts[0]
            log_level = parts[1]
            message = ' - '.join(parts[2:]).strip()
            log_data.append({
                'Timestamp': timestamp,
                'LogLevel': log_level,
                'Message': message
            })

    return log_data


###--------------------------------->>>>>>>
# writes parsed log data into a CSV file with a timestamped filename
def logToCsv(log_data, LOG_OUTPUT):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{timestamp}-log-data.csv"
    output_file = os.path.join(LOG_OUTPUT, filename)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            'Timestamp',
            'LogLevel', 
            'Message'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in log_data:
            writer.writerow(entry)

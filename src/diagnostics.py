from datetime import datetime
import csv
import glob
import json
import os
import time

class Diagnostics:

    def __init__(self):
        
        # run time
        self.date = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        # data output files
        self.log_file = None
        self.site_file = None
        self.word_file = None 
        # data output file size
        self.log_file_size = None
        self.site_file_size = None
        self.word_file_size = None
        # word data metrics
        self.total_words = 0
        self.unique_words = 0
        self.sum_counts = 0
        # site data metrics
        self.sum_image_count = 0
        self.sum_link_count = 0
        self.sum_stylesheet_count = 0
        self.sum_script_count = 0
        # log data metrics
        self.urls_attempted = 0
        self.url_timeouts = 0
        self.disallowed_skip_count = 0
        self.level_info_count = 0
        self.level_warning_count = 0
        self.level_error_count = 0
        self.robot_log_count = 0
        self.utility_log_count = 0
        self.scraper_log_count = 0


    ###--------------------------------->>>>>>>
    # 
    def start(self):
        self.start_time = time.time()
        self.date = datetime.now().strftime("%m-%d-%Y")
        print('''
    Welcome to Website Words!

    Start Console ---------------------------------------------------------------------]
    |  -Require file:   Diagnostics.py   produces diagnostic summary JSON file
    |  -Require file:   Scraper.py       produces site and word data CSV files
    |  -Require file:   Utility.py       sets up project structure, reads, writes, sorts
    |  -Require file:   Robots.py        obtains site permissions for crawling
    |  -Require file:   Logparser.py     produces log data CSV file
            
    Running Website Words!
        ''')


    ###--------------------------------->>>>>>>
    #
    def end(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print('''
    Finishing Website Words!
            
    End Console -----------------------------------------------------------------------]
    |  -Wrote file:   *-word-data.csv
    |  -Wrote file:   *-site-data.csv
    |  -Wrote file:   *-log-data.csv
    |  -Writing...    *-diagnostic-summary.json   
            
    Exiting Website Words!
        ''')


    ###--------------------------------->>>>>>>
    # 
    def summary(self):
        self.assignDataFiles()
        self.recordFileSizes()
        self.calculateWordMetrics()
        self.calculateSiteMetrics() 
        self.calculateLogMetrics()
        self.processDiagnosticSummary()
        self.correctBadTimestamp()


    ###--------------------------------->>>>>>>
    # 
    def assignDataFiles(self):
        word_files = glob.glob('data/output/*-word-data.csv')
        if word_files:
            self.word_file = max(word_files, key=os.path.getctime)

        site_files = glob.glob('data/output/*-site-data.csv')
        if site_files:
            self.site_file = max(site_files, key=os.path.getctime)

        log_files = glob.glob('data/output/*-log-data.csv')
        if log_files:
            self.log_file = max(log_files, key=os.path.getctime)


    ###--------------------------------->>>>>>>
    # 
    def recordFileSizes(self):

        if self.word_file and os.path.exists(self.word_file):
            self.word_file_size = os.path.getsize(self.word_file)
        
        if self.site_file and os.path.exists(self.site_file):
            self.site_file_size = os.path.getsize(self.site_file)
        
        if self.log_file and os.path.exists(self.log_file):
            self.log_file_size = os.path.getsize(self.log_file)


    ###--------------------------------->>>>>>>
    # 
    def calculateWordMetrics(self):

        if self.word_file and os.path.exists(self.word_file):
            
            with open(self.word_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)
                word_index = header.index('Word')
                count_index = header.index('Count')
                unique_words_set = set()

                for row in reader:
                    word = row[word_index]
                    unique_words_set.add(word)
                    count = int(row[count_index])
                    self.sum_counts += count
                    self.total_words += 1

                self.unique_words = len(unique_words_set)


    ###--------------------------------->>>>>>>
    # 
    def calculateSiteMetrics(self):

        if self.site_file and os.path.exists(self.site_file):

            with open(self.site_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.sum_image_count += int(row.get('ImageCount', 0))
                    self.sum_link_count += int(row.get('LinkCount', 0))
                    self.sum_stylesheet_count += int(row.get('StylesheetCount', 0))
                    self.sum_script_count += int(row.get('ScriptCount', 0))


    ###--------------------------------->>>>>>>
    # 
    def calculateLogMetrics(self):

        if self.log_file and os.path.exists(self.log_file):

            with open(self.log_file, 'r', encoding='utf-8') as file:

                for line in file:

                    if "R-" in line:
                        self.robot_log_count += 1
                    elif "U-" in line:
                        self.utility_log_count += 1
                    else:
                        self.scraper_log_count += 1
                    
                    if "INFO" in line:
                        self.level_info_count += 1
                    elif "WARNING" in line:
                        self.level_warning_count += 1
                    elif "ERROR" in line:
                        self.level_error_count += 1

                    if "Successfully fetched" in line or "Error fetching" in line:
                        self.urls_attempted += 1
                    
                    if "Max retries exceeded" in line or "SSLError" in line:
                        self.url_timeouts += 1

                    if "due to disallowed path" in line:
                        self.disallowed_skip_count += 1


    ###--------------------------------->>>>>>>
    # writes diagnostic summary data to a JSON file
    def processDiagnosticSummary(self):
        summary_data = {
            "run_time": {
                "Date": self.date,
                "StartTime": self.start_time,
                "EndTime": self.end_time,
                "Duration": self.duration,
            },
            "data_output": {
                "LogFile": self.log_file,
                "SiteFile": self.site_file,
                "WordFile": self.word_file,
                "LogFileSizeB": self.log_file_size,
                "SiteFileSizeB": self.site_file_size,
                "WordFileSizeB": self.word_file_size
            },
            "word_metrics": {
                "TotalWords": self.total_words,
                "UniqueWords": self.unique_words,
                "SumCounts": self.sum_counts
            },
            "site_metrics": {
                "SumImageCount": self.sum_image_count,
                "SumLinkCount": self.sum_link_count,
                "SumStylesheetCount": self.sum_stylesheet_count,
                "SumScriptCount": self.sum_script_count
            },
            "log_metrics": {
                "UrlsAttempted": self.urls_attempted,
                "UrlTimeouts": self.url_timeouts,
                "DisallowedSkipCount": self.disallowed_skip_count,
                "LevelInfoCount": self.level_info_count,
                "LevelWarningCount": self.level_warning_count,
                "LevelErrorCount": self.level_error_count,
                "RobotLogCount": self.robot_log_count,
                "UtilityLogCount": self.utility_log_count,
                "ScraperLogCount": self.scraper_log_count
            }
        }

        timestamp = '-'.join(os.path.basename(self.word_file).split('-')[0:2])
        output_file = os.path.join('data/output', f'{timestamp}-diagnostic-summary.json')

        with open(output_file, 'w', encoding='utf-8') as summary_file:
            json.dump(summary_data, summary_file, indent=4)

    
    ###--------------------------------->>>>>>>
    # 
    def correctBadTimestamp(self):
        goode_timestamp = '-'.join(os.path.basename(self.word_file).split('-')[:2])
        files_to_check = [self.log_file, self.site_file]

        for file in files_to_check:

            if file:
                current_timestamp = '-'.join(os.path.basename(file).split('-')[:2])

                if current_timestamp != goode_timestamp:
                    update = file.replace(current_timestamp, goode_timestamp)
                    os.rename(file, update)
                    print(f'Corrected bad timestamp for {file}')
        
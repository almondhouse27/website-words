import csv
import glob
import json
import os
import time

class Diagnostics:

    def __init__(self):
        
        # run time
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
        # log data metrics
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
        print('''
        Welcome to Website Words!

        Start Console -----------------------]
        |  -Starting:  Diagnostics
        |  -Starting:  Scraper
        |  -Starting:  Utility
        |  -Starting:  Robots
        |  -Starting:  Logparser
            
        Running Website Words!
        ''')


    ###--------------------------------->>>>>>>
    #
    def end(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print('''
        Finishing Website Words!
            
        End Console -------------------------]
        |  -Writing:  *-word-data.csv
        |  -Writing:  *-site-data.csv
        |  -Writing:  *-log-data.csv
        |  -Writing:  *-diagnostic-summary.csv
            
        Exiting Website Words! ~take care
        ''')


    ###--------------------------------->>>>>>>
    # 
    def summary(self):
        self.assignDataFiles()
        self.recordFileSizes()
        self.calculateWordMetrics()
        self.trackLogSource()
        self.processDiagnosticSummary()


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
    def trackLogSource(self):

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


    ###--------------------------------->>>>>>>
    # writes diagnostic summary data to a JSON file
    def processDiagnosticSummary(self):
        summary_data = {
            "run_time": {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.duration,
            },
            "data_output": {
                "log_file": self.log_file,
                "site_file": self.site_file,
                "word_file": self.word_file,
                "log_file_size": self.log_file_size,
                "site_file_size": self.site_file_size,
                "word_file_size": self.word_file_size
            },
            "word_metrics": {
                "total_words": self.total_words,
                "unique_words": self.unique_words,
                "sum_counts": self.sum_counts
            },
            "log_metrics": {
                "level_info_count": self.level_info_count,
                "level_warning_count": self.level_warning_count,
                "level_error_count": self.level_error_count,
                "robot_log_count": self.robot_log_count,
                "utility_log_count": self.utility_log_count,
                "scraper_log_count": self.scraper_log_count
            }
        }

        timestamp = '-'.join(os.path.basename(self.log_file).split('-')[0:2])
        output_file = os.path.join('data/output', f'{timestamp}-diagnostic-summary.json')

        with open(output_file, 'w', encoding='utf-8') as summary_file:
            json.dump(summary_data, summary_file, indent=4)

        
import os
import time
import json
import pandas as pd
from datetime import datetime


class Diagnostics:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.log_file = 'logs/scraper.log'
        self.word_data_file = None
        self.site_data_file = None
        self.urls_attempted = 0
        self.urls_succeeded = 0
        self.urls_timed_out = 0
        self.urls_no_connection = 0
        self.disallowed_skip_count = 0
        self.request_times = []
        self.total_word_count = 0
        self.unique_word_count = 0
        self.level_info_count = 0
        self.level_warning_count = 0
        self.level_error_count = 0

    
    ###--------------------------------->>>>>>>
    # log data
    def parse_log_levels(self):

        with open(self.log_file, 'r') as file:
            logs = file.readlines()
            self.level_info_count = sum(1 for log in logs if 'INFO' in log)
            self.level_warning_count = sum(1 for log in logs if 'WARNING' in log)
            self.level_error_count = sum(1 for log in logs if 'ERROR' in log)

    def calculate_word_counts(self):

        if self.word_data_file and os.path.exists(self.word_data_file):
            df = pd.read_csv(self.word_data_file)
            self.total_word_count = df.shape[0]
            self.unique_word_count = df['word'].nunique()

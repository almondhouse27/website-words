
# WEBSITE WORDS 
### a python web scraper
#### developed by David Blessent (almondhouse27)

## Summary

*The web scraper project is designed to automate the extraction of textual data from specified websites, analyzing and organizing that data for further processing. It is structured into multiple components, each responsible for specific tasks, ensuring modularity and maintainability.*

**Core Functionality:** The primary goal of the scraper is to gather textual content from websites, count words, and gather various metrics about the sites visited. It accomplishes this by utilizing a combination of HTTP requests and HTML parsing.

**Project Structure and Setup:** The setupProjectStructure() function initializes the project environment, checks for necessary directories, verifies the existence of a backup input file, and installs required Python packages specified in requirements.txt. This ensures that the project can run smoothly on different systems without manual setup.

**Data Input and Output:** The scraper reads URLs from a CSV file using the readDataInput() function, and it generates two types of output files: word count data (word-data.csv) and site details (site-data.csv). Each of these outputs includes comprehensive information gathered from the sites, such as word counts and various site metrics (e.g., number of images, links, scripts).

**Logging and Diagnostics:** The project incorporates robust logging features to monitor its execution and capture any issues encountered during the scraping process. The Diagnostics class tracks performance metrics, including runtime duration, file sizes, and counts of specific log events (e.g., errors, warnings). It also generates a summary report in JSON format, providing insights into the scraper's performance and the data collected.

**Robots.txt Compliance:** The scraper respects web crawling best practices by checking the robots.txt file for each domain to determine allowed paths for scraping. This is handled through the robotCheckpoint() and checkPermissions() functions, ensuring that the scraper only accesses permitted content.

**Data Parsing and Output Formatting:** The parseScraperLog() and logToCsv() functions format log data into structured CSV files, facilitating easy analysis of the scraper's operations and outcomes. This is essential for evaluating the efficiency and effectiveness of the scraping process.

*Overall, this web scraper project employs a comprehensive and systematic approach to web data extraction, ensuring compliance with web standards while providing valuable insights through detailed analytics and metrics. Its modular design allows for easy updates and enhancements, making it a versatile tool for web data mining.*

## Breakdown

*This Python web scraper is designed to extract data from websites and produce structured outputs in CSV and JSON formats. Here’s a breakdown of how it works and what it produces:*

### Key Components:

#### Dependencies

Requests: 
- *Used to send HTTP requests to websites and handle responses.*

BeautifulSoup: 
- *Parses HTML content from the website's response, allowing for easy extraction and manipulation of data.*

Robots: 
- *Checks robots.txt files to respect scraping permissions, ensuring compliance with the website’s rules regarding automated access.*

Diagnostics: 
- *Tracks runtime performance, calculates metrics, and generates a comprehensive summary of the scraping process.*

Logparser: 
- *Parses logs into a CSV format, providing a structured view of runtime information and issues encountered during the scraping operation.*

#### Functionality

**Scrape Websites (scrapeWebsite):**

HTTP Request Handling: 
- *Sends an HTTP request to a provided URL.*
- *Checks the site's robots.txt file to ensure compliance with web scraping permissions before proceeding.*

Data Extraction:
- *Extracts the text content of the page, counts word occurrences, and collects website structure details (e.g., number of images, links, scripts, stylesheets, forms, etc.).*
- *Returns two dictionaries: one for word frequencies and one for structural details.*

**Execute Website Words (executeWebsiteWords):**

Reads URLs from an input CSV file (url-list.csv):
- *For each website, it checks its robots.txt for disallowed paths and skips scraping if necessary.*
- *Scrapes each website for text and site details.*

Writes three output CSV files:
- *word-data.csv*
- *site-data.csv*
- *log-data.csv*

Additionally: *the function converts the log file into log-data.csv using a log parser and sorts the output files*

**Runtime Diagnostics (class Diagnostics):**

Tracks and logs performance metrics, including request outcomes and script runtime, in a JSON file 
- *diagnostic-summary.json*

#### Output

**The scraper produces four timestamped output files**

word-data.csv: 
- *Lists all words found on the scraped websites with their frequency counts.*

site-data.csv: 
- *Contains metadata about the website's structure (e.g., image count, links, scripts, stylesheets, forms, etc.).*

log-data.csv: 
- *A CSV version of the runtime log, capturing key events like requests, errors, and other log details.*
diagnostic-summary.json: Provides a summary of the scraper's runtime performance, including descriptive statistics of word data and log details.

#### Final Summary

*In essence, this web scraper is designed to extract both content (words) and structure (site details) from websites while respecting robots.txt rules and tracking the execution process in logs and diagnostics. It efficiently compiles and organizes the gathered data into structured output files for further analysis.*




Overview of requirements.txt
The requirements.txt file is a standard convention in Python projects that lists all the dependencies required to run the application. Each line specifies a package name and optionally its version, allowing developers to manage and replicate the environment needed for the project easily. This file simplifies the installation process for new developers or when deploying the application by ensuring that all necessary packages are installed in the correct versions.

Automatic Installation in setupProjectStructure()
In the setupProjectStructure() function, the following command is executed to install the dependencies specified in the requirements.txt file:

python
Copy code
subprocess.check_call([
    os.sys.executable,
    '-m', 'pip', 'install', '-r', 'requirements.txt'],
    stdout=devnull,
    stderr=devnull
)
This command utilizes the Python interpreter (specified by os.sys.executable) to run the pip module, which manages Python packages. The install command is issued with the -r flag, pointing to requirements.txt, thereby checking if each listed dependency is already installed and installing it if it is not.

Purpose of Specific Libraries
BeautifulSoup4 (beautifulsoup4==4.12.3): BeautifulSoup is a Python library for parsing HTML and XML documents. It creates parse trees that allow for easy data extraction from web pages, making it a valuable tool for web scraping and data manipulation.

Requests (requests==2.32.3): The Requests library simplifies making HTTP requests in Python, allowing developers to send HTTP requests with ease and handle responses. It abstracts the complexities of the underlying urllib library, making it user-friendly for tasks such as fetching web pages or interacting with APIs.

Pandas (pandas==2.2.3): Pandas is a powerful data manipulation and analysis library that provides data structures like DataFrames for handling structured data. It offers a wide range of functions for data cleaning, transformation, and analysis, making it an essential tool for data scientists and analysts in Python.














Summary of the Utility Module:
This utility module provides helper functions to manage project structure, read and write data to CSV files, and handle the sorting of the output. Here’s how each function works and what it contributes:

Key Components:
Project Setup (setupProjectStructure):

Ensures the project directories and input files exist. If they don’t, it creates the necessary directories and copies a backup input file (url-list.csv).
Clears or creates the log file.
Installs project dependencies by running pip with requirements.txt.
Logs actions like directory creation, input file backup, and errors encountered during the setup process.
Reading Data (readDataInput):

Reads the URLs and associated metadata (Category, State, City, Institution) from a CSV file (url-list.csv).
Returns a dictionary where the key is the website URL and the value is metadata about that website (institution, category, location).
Writing Word Data (writeWordData):

Takes in word frequency data (for each website) and writes it to a timestamped CSV file (word-data.csv).
Each row in the CSV file contains a website URL, a word, and the count of that word on the site.
Logs whether the data was successfully saved or if there were errors during the process.
Writing Site Data (writeSiteData):

Writes the structural details of each website (such as image count, link count, title, and description) to a timestamped CSV file (site-data.csv).
Includes metadata like the institution, category, and location.
Logs success or failure of saving the data to a file.
Sorting Output Files (sortDataOutput):

After writing the word and site data files, this function sorts the data for easier readability.
Word data is sorted by website and word, while site data is sorted by the website.
Updates the output CSV files with the sorted data and logs the operation.
Outputs:
word-data.csv: Contains word frequencies for each website.
site-data.csv: Contains structural details about each website, such as image count, link count, etc.
Logs: Logs are maintained for various actions (like file creation, errors, etc.) during the execution of these utility functions.
Overall, this utility module plays a vital role in preparing the project structure, reading inputs, managing the output of scraped data, and ensuring the data is structured properly in CSV files.





Summary of the Diagnostics Class:
This class is designed to track and analyze the execution of a web scraping project, providing metrics on the word and site data collected, as well as logs related to the process. It calculates various metrics, records them in a JSON file, and checks for timestamp consistency across files. Here’s a breakdown of its functionality:

Key Components:
Attributes:
Run Time: Tracks the start time, end time, and duration of the process.
Data Output Files: Holds the filenames of log, site, and word data files.
File Sizes: Records the sizes of these output files.
Word Data Metrics: Tracks total words, unique words, and the sum of word counts.
Site Data Metrics: Records totals for images, links, stylesheets, and scripts.
Log Data Metrics: Counts the number of attempted URLs, timeouts, disallowed skips, and log levels (info, warning, error), and categorizes logs (robot, utility, scraper).
Key Methods:
start():

Initiates the diagnostics by recording the start time and printing an introduction message. This method marks the beginning of the data collection.
end():

Marks the end of the process by capturing the end time and printing a summary of the output. It serves as a conclusion to the diagnostics process, signaling when the data collection is complete.
summary():

Executes a series of operations to collect data metrics, assign filenames, record file sizes, calculate word and site data metrics, and process the diagnostic summary JSON file.
assignDataFiles():

Locates the latest output files for word data, site data, and logs, and assigns them to the respective attributes (word_file, site_file, log_file).
recordFileSizes():

Records the file sizes for the output files, helping to track the volume of data processed.
calculateWordMetrics():

Calculates word metrics by counting the total number of words, unique words, and the sum of word counts from the word data CSV file.
calculateSiteMetrics():

Calculates site metrics by summing up the number of images, links, stylesheets, and scripts across all websites from the site data CSV file.
calculateLogMetrics():

Processes the log file to calculate various metrics, such as the number of URLs attempted, timeouts, disallowed skips, and counts for different log levels (info, warning, error). It also categorizes logs into robot, utility, and scraper logs.
processDiagnosticSummary():

Writes all the calculated metrics to a JSON file (diagnostic-summary.json). The file contains run-time data, file sizes, word and site metrics, and log statistics.
correctBadTimestamp():

Ensures that all output files (log, site, word) have consistent timestamps. If a file has a mismatched timestamp, it corrects it by renaming the file with the correct timestamp.
Outputs:
diagnostic-summary.json: Contains a detailed summary of the run-time, file sizes, word data, site data, and log metrics.
Logs: Keeps track of different log metrics and ensures that the process is well-documented.
Purpose:
The Diagnostics class is crucial for evaluating the performance of a web scraping project, providing insights into the amount of data processed, error rates, and the time taken to complete the process. It also ensures the integrity of output file timestamps, ensuring consistency across files.





Summary of the Robots Checkpoint Module
This module is designed to check the robots.txt file of a given domain to determine if there are any restrictions on web scraping activities. It uses the requests library to fetch the robots.txt file and parses it to extract disallowed paths.

Key Functions:
robotCheckpoint(domain):

Constructs the URL for the robots.txt file using both HTTP and HTTPS protocols.
Attempts to fetch the robots.txt file for the specified domain.
Logs a success message if the file is successfully retrieved, returning its contents.
If the fetch fails for both protocols, logs a warning message and returns None.
checkPermissions(url):

Extracts the domain from the provided URL.
Calls robotCheckpoint() to retrieve the robots.txt file for the domain.
If no robots.txt is found, logs a warning and assumes no restrictions on scraping.
Parses the contents of the robots.txt file, looking for user-agent directives and disallowed paths.
Logs the disallowed paths for the domain and returns them as a list.
Purpose:
The module helps web scrapers comply with the directives set by websites in their robots.txt files. By identifying disallowed paths, it aids in ensuring that scraping activities are conducted ethically and legally, reducing the risk of being blocked or encountering legal issues.






Summary of the Log Parser Module
This module is designed to parse runtime log data from a specified log file (logs/scraper.log) and convert it into a structured CSV format. The output file is timestamped and stored in a specified output directory.

Key Functions:
executeLogParser(LOG_FILE, LOG_OUTPUT):

Main function that orchestrates the log parsing process.
Calls readScraperLog() to read the log lines from the specified log file.
Calls parseScraperLog() to convert the log lines into structured data.
Calls logToCsv() to write the structured log data to a CSV file.
readScraperLog(LOG_FILE):

Reads the contents of the specified log file and returns the lines as a list.
Utilizes the readlines() method to capture all log entries.
parseScraperLog(log_lines):

Parses each log line into a structured format by splitting the line into its components: timestamp, log level, and message.
Creates a list of dictionaries, each containing the parsed data.
logToCsv(log_data, LOG_OUTPUT):

Writes the structured log data into a CSV file.
Generates a filename using the current timestamp and saves it in the specified output directory.
Utilizes csv.DictWriter to write the header and each log entry to the CSV file.
Purpose:
The module automates the process of extracting and structuring log data, making it easier to analyze runtime behavior, track issues, and maintain records. By converting logs into a CSV format, it facilitates further data manipulation and visualization using spreadsheet applications or data analysis tools.











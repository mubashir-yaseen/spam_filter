import csv
import re
from DB.DatabaseDriver import DatabaseDriver
class URLAnalyzer:
    def __init__(self):
        driver = DatabaseDriver()
        self.blacklist_urls = driver.FetchURL()

    def check_url_in_blacklist(self, url):
        # Check if the URL is in the blacklist
        return url in self.blacklist_urls

def read_column_from_csv(csv_file, column_name):
    column_values = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Check if the column exists in the CSV header
        if column_name not in reader.fieldnames:
            print(f"Column '{column_name}' not found in the CSV file.")
            return []

        # Read each row and append the value of the specified column to the list
        for row in reader:
            column_values.append(row[column_name])

    return column_values

def extract_urls_from_email_body(email_body):
    # Regular expression pattern to match URLs
    url_pattern = r'\b(?:https?://|www\.)\S+\b'

    # Find all URLs in the email body
    urls = re.findall(url_pattern, email_body)

    return urls


incoming_email_body = read_column_from_csv('CSV/SpamAssasin.csv', 'body')
blacklist_urls = extract_urls_from_email_body(incoming_email_body[0])

#urls = ["https://phishing.net/login", "https://legit.com"]
url_analyzer = URLAnalyzer()

# Analyze URLs for potential threats
for url in blacklist_urls:
    is_blacklisted = url_analyzer.check_url_in_blacklist(url)
    if is_blacklisted:
        print(f"URL {url} is in the blacklist and may be malicious.")
    else:
        print(f"URL {url} is not in the blacklist.")
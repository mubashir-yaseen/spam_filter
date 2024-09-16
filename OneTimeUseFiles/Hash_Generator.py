import csv
import hashlib
import re
from DB.DatabaseDriver import DatabaseDriver


def generate_hash(email):
    # Generate a unique hash for the email message
    hash_object = hashlib.sha256(email.encode())
    return hash_object.hexdigest()


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


def write_hash_to_DB(email_list):
    driver = DatabaseDriver()
    for email in email_list:
        hash = generate_hash(email)
        driver.StoreHash(hash)


def write_urls_to_DB(url_list):
    driver = DatabaseDriver()
    for url in url_list:
        driver.StoreURL(url)


def extract_urls_from_email_body(email_body):
    # Regular expression pattern to match URLs
    url_pattern = r'\b(?:https?://|www\.)\S+\b'

    # Find all URLs in the email body
    url = re.findall(url_pattern, email_body)

    return url


# Main Code
csv_file = '../CSV/SpamAssasin.csv'
column_name = 'body'

email_list = read_column_from_csv(csv_file, column_name)

urls = []
for body in email_list:
    urls.extend(extract_urls_from_email_body(body))

write_hash_to_DB(email_list)
write_urls_to_DB(urls)

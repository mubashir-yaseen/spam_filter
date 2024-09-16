import csv
import hashlib
from DB.DatabaseDriver import DatabaseDriver

# Class for Email Hash Searching
class EmailVerifier:
    def __init__(self, hashed_csv):
        self.phishing_hash_database = []
        self.hashed_csv = hashed_csv

    def generate_hash(self, email_message):
        # Generate a unique hash for the email message
        hash_object = hashlib.sha256(email_message.encode())
        return hash_object.hexdigest()

    # Full Check
    def check_phishing(self, email_message):
        # Generate hash for the incoming email
        email_hash = self.generate_hash(email_message)
        print(email_hash)
        # Check if the hash exists in the phishing hash database
        if email_hash in self.phishing_hash_database:
            return True
        else:
            return False

    def fetch_hashed_emails(self):
        driver = DatabaseDriver()
        hashed_emails = driver.FetchHash()
        self.phishing_hash_database = hashed_emails

    def read_column_from_csv(self, csv_file, column_name):
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

    # Percentage Check
    def calculate_similarity(self, email_hash):
        similarity = 0.0

        for email in self.phishing_hash_database:
            total = len(email[0])
            length = 0
            count = 0
            if len(email_hash) > len(email[0]):
                length = len(email[0])
            else:
                length = len(email_hash)
            for i in range(length):
                if email_hash[i] == email[i]:
                    count += 1
            similar = (count/length)*100
            if similar > similarity:
                similarity = similar

        if similarity > 80:
            self.append_hashes_to_csv(email_hash)
        return similarity

    def compare_hashes(self, email_list):
        email_hash = self.generate_hash(email_list)
        similarity = self.calculate_similarity(email_hash)
        return similarity

    def append_hashes_to_csv(self, email_hash):
        driver = DatabaseDriver()
        driver.StoreHash(email_hash)

emailverifier = EmailVerifier('CSV/hashed_emails.csv')
emailverifier.fetch_hashed_emails()
incoming_email = emailverifier.read_column_from_csv('CSV/SpamAssasin.csv', 'body')

# Check if the incoming email is phishing
similarities = emailverifier.compare_hashes(incoming_email[0])

if similarities > 80:
    print("This email is identified as phishing.")
else:
    print("This email is not identified as phishing.")

import dns.resolver
import csv
import re
import logging
import hashlib
import base64
import hmac

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class EmailAuthenticationAnalyzer:
    def __init__(self):
        pass

    def check_spf(self, sender_domain):
        try:
            answers = dns.resolver.resolve(sender_domain, 'TXT')
            for rdata in answers:
                spf_data = rdata.strings[0].decode('utf-8')
                if spf_data.startswith('v=spf'):
                    return self.analyze_spf_record(spf_data)
            return False
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False

    def analyze_spf_record(self, spf_data):
        parts = spf_data.split()
        mechanisms = parts[1:]
        for mechanism in mechanisms:
            if mechanism.startswith('ip'):
                ip_range = mechanism.split(':')[1]
                return True
        return False

    def check_dkim(self, email_body):
        dkim_signature = self.extract_dkim_signature(email_body)
        if not dkim_signature:
            return False
        match = re.match(r's=(.*?);', dkim_signature)
        if not match:
            return False
        signing_domain = match.group(1)
        match = re.match(r'b=(.*?);', dkim_signature)
        if not match:
            return False
        signature = match.group(1)
        public_key = self.retrieve_public_key(signing_domain)
        if not public_key:
            return False
        hashed_message = hashlib.sha256(email_body.encode()).digest()
        decoded_signature = base64.b64decode(signature)
        return hmac.compare_digest(decoded_signature, hashed_message)

    def retrieve_public_key(self, signing_domain):
        try:
            selector = "selector1"
            query = selector + "._domainkey." + signing_domain
            answers = dns.resolver.resolve(query, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    if txt_string.startswith("v=DKIM1"):
                        return txt_string.split(";")[1].split("=")[1]
            return None
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return None

    def extract_dkim_signature(self, email_body):
        logging.debug("Raw Email Body:")
        logging.debug(email_body)  # Print raw email body for debugging

        # Attempt to split headers and body
        try:
            headers, body = email_body.split('\n\n', 1)
        except ValueError as e:
            logging.error("Failed to split email body into headers and body: %s", e)
            logging.debug("Full Email Body Content:")
            logging.debug(email_body)
            return None

        logging.debug("Email Headers:")
        logging.debug(headers)

        # Adjusted regex pattern for DKIM signature extraction
        pattern = re.compile(r'DKIM-Signature:.*?s=([^;]+);.*?b=([^;]+);', re.DOTALL | re.IGNORECASE)
        match = pattern.search(headers)
        if match:
            return f's={match.group(1)};b={match.group(2)};'.strip()
        else:
            logging.debug("DKIM Signature header not found.")
            return None

def read_column_from_csv(csv_file, column_name):
    column_values = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if column_name not in reader.fieldnames:
            print(f"Column '{column_name}' not found in the CSV file.")
            return []
        for row in reader:
            column_values.append(row[column_name])
    return column_values

email_analyzer = EmailAuthenticationAnalyzer()

incoming_email_body = read_column_from_csv('CSV/SpamAssasin.csv', 'body')
incoming_email_sender = read_column_from_csv('CSV/SpamAssasin.csv', 'sender')
parts = incoming_email_sender[0].split("@")
sender = parts[1].split(">")
print(sender[0])
sender_domain = sender[0]
email_body = incoming_email_body[0]

spf_authentication_result = email_analyzer.check_spf(sender_domain)
dkim_authentication_result = email_analyzer.check_dkim(email_body)
print("SPF Authentication Result:", spf_authentication_result)
print("DKIM Authentication Result:", dkim_authentication_result)

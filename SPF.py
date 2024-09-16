import dns.resolver
import csv
import re

class EmailAuthenticationAnalyzer:
    def __init__(self):
        pass
    def check_spf(self, sender_domain):
        # Perform DNS query to retrieve SPF record
        try:
            answers = dns.resolver.resolve(sender_domain, 'TXT')
            for rdata in answers:
                # Check if the TXT record contains SPF data
                spf_data = rdata.strings[0].decode('utf-8')
                if spf_data.startswith('v=spf'):
                    # Parse and analyze SPF data
                    return self.analyze_spf_record(spf_data)
            return False  # No SPF record found
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False  # DNS query failed

    def analyze_spf_record(self, spf_data):
        # Parse and analyze SPF data
        parts = spf_data.split()
        mechanisms = parts[1:]

        # Check if the sender's IP is allowed by any mechanism in the SPF record
        for mechanism in mechanisms:
            if mechanism.startswith('ip'):
                ip_range = mechanism.split(':')[1]
                return True
        return False

    def check_dkim(self, email_body):
        # Extract DKIM signature from email headers
        dkim_signature = self.extract_dkim_signature(email_body)

        # Verify DKIM signature presence
        if not dkim_signature:
            return False

        # Extract DKIM signature fields
        match = re.match(r's=(.*?);', dkim_signature)
        if not match:
            return False
        signing_domain = match.group(1)

        match = re.match(r'b=(.*?);', dkim_signature)
        if not match:
            return False
        signature = match.group(1)

        # Retrieve DKIM public key
        public_key = self.retrieve_public_key(signing_domain)
        if not public_key:
            return False

        # Verify DKIM signature
        hashed_message = hashlib.sha256(email_body.encode()).digest()
        decoded_signature = base64.b64decode(signature)
        return hmac.compare_digest(decoded_signature, hashed_message)

    def retrieve_public_key(self, signing_domain):
        # Perform DNS query to retrieve DKIM public key
        try:
            selector = "selector1"  # Example selector, you may need to extract it from the DKIM signature
            query = selector + "._domainkey." + signing_domain
            answers = dns.resolver.resolve(query, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    if txt_string.startswith("v=DKIM1"):
                        # Extract public key from DKIM record
                        # Example: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC54S69oifdRIfu4tDsiMWXvsqeFV5fNxd+EdExO+D6RPHwT/cWZ39tGeg9Bpr6z8CAzj2vRGLj7I7kdJ8PHDlkDNuRcLdYll8HZjRb75E4xVxGjBtXTiFDx/m1K4T9Eqyw/qc5vR9JhW/7+bY4Jkg7szTSx5c6o9wN26Hv0IiTQIDAQAB
                        return txt_string.split(";")[1].split("=")[1]
            return None
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return None

    def extract_dkim_signature(self, email_body):
        # Search for DKIM-Signature header in the email body
        match = re.search(r'DKIM-Signature:\s*(.*?)(?=\n\S)', email_body, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return None



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


email_analyzer = EmailAuthenticationAnalyzer()

incoming_email_body = read_column_from_csv('CSV/SpamAssasin.csv', 'body')
incoming_email_sender = read_column_from_csv('CSV/SpamAssasin.csv', 'sender')
parts = incoming_email_sender[0].split("@")
sender = parts[1].split(">")
print(sender[0])
sender_domain = sender[0]
email_body = incoming_email_body[0]

# Analyze email authentication using SPF
spf_authentication_result = email_analyzer.check_spf(sender_domain)
dkim_authentication_result = email_analyzer.check_dkim(email_body)
print("SPF Authentication Result:", spf_authentication_result)
print("DKIM Authentication Result:", dkim_authentication_result)



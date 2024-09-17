from URL_Analyzer import URLAnalyzer, extract_urls_from_email_body

def process_email(email_body):
    url_analyzer = URLAnalyzer()  # Create an instance of URLAnalyzer
    urls = extract_urls_from_email_body(email_body)  # Extract URLs from the email body
    
    for url in urls:
        if url_analyzer.check_url_in_blacklist(url):
            print(f"URL {url} is blacklisted and may be malicious.")
        else:
            print(f"URL {url} is not blacklisted.")

# Example usage
if __name__ == "__main__":
    sample_email_body = "Visit our website at http://example.com and check http://malicious.com"
    process_email(sample_email_body)

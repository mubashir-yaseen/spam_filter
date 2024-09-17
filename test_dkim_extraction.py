import re

def extract_dkim_signature(email_body):
    match = re.search(r'DKIM-Signature:\s*(.*?)\r?\n', email_body, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        print("DKIM Signature header not found.")
        return None

# Test with different sample email bodies
sample_email_bodies = [
    """
    DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=example.com; s=selector;
    b=sampleSignature==;
    ...
    """,
    """
    Some other headers
    DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=anotherdomain.com; s=anotherselector;
    b=anotherSignature==;
    ...
    """
]

for body in sample_email_bodies:
    signature = extract_dkim_signature(body)
    print(f"Extracted DKIM Signature: {signature}")

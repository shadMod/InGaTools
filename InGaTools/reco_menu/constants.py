RECO_MENU = """What do you want to do?

    1. Get Header Information
    2. Get SSL Certificate Information
    3. Get Whois Lookup
    4. Get Sub-domain Website
    5. Crawl Target Website (includes Email, Sub-Domain, File Type, etc...)
    6. Test All Available Options
    0. To exit
"""

# --------------------------------- RECO FIELD LIST ---------------------------------------
SSL_INFO_FIELD_LIST = [
    ("Version", "version"),
    ("Serial Number", "serialNumber"),
    ("Not Before", "notBefore"),
    ("Not After", "notAfter"),
    ("OCSP", "OCSP"),
    ("Subject Alt Name", "subjectAltName"),
    ("CA Issuers", "caIssuers"),
    ("CRL Distribution Points", "crlDistributionPoints"),
]

WHOIS_LOOKUP_FIELD_LIST = [
    ("NIR", "nir"),
    ("ASN Registry", "asn_registry"),
    ("ASN", "asn"),
    ("ASN CIDR", "asn_cidr"),
    ("ASN Country Code", "asn_country_code"),
    ("ASN Date", "asn_date"),
    ("ASN Description", "asn_description"),
]

# ----------------------------------- ERROR LIST ------------------------------------------
FINDER_URL = "https://www.virustotal.com/vtapi/v2/domain/report"
SSL_KEY_ERROR = "KeyError on Target URL."
SSL_NOT_FOUND = "SSL is not Present on Target URL."
CHOICE_NOT_ALLOWED = "Choice not allowed, try again."

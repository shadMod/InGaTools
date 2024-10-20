import os

DEBUG = os.getenv("DEBUG", False)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY", None)

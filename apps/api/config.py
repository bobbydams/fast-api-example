import os

from dotenv import load_dotenv

load_dotenv("var/.env")


def get_database_uri():
    return os.getenv("DATABASE_URI")
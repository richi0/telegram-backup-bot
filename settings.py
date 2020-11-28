import os
from dotenv import load_dotenv

# Load the environmet variables from the .env file
load_dotenv()

password = os.getenv("PASSWORD")
token = os.getenv("TOKEN")
file_location = os.getenv("FILE_LOCATION")
db_logging = bool(int(os.getenv("DBLOGGING")))

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file

openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPAPI_API_KEY"] = serpapi_api_key
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingfacehub_api_token

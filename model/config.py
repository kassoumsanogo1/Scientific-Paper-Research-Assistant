# config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
    IEEE_API_KEY = os.getenv("IEEE_API_KEY")
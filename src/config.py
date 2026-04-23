# config.py - Centralized configuration and setup for the Slack Co-Pilot app
# config.py holds all init and shared state for the app, including:
# - Slack and Flask app setup
# - Groq client setup
# - MongoDB connection
# It also defines constants like MIN_QUESTIONS and MAX_QUESTIONS, and a debug function for logging.

import os
from flask import Flask
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from pymongo import MongoClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

MIN_QUESTIONS = 7
MAX_QUESTIONS = 10

# Slack + Flask
bolt_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# MongoDB
mongo = MongoClient(MONGO_URI)
db = mongo["slack_co_pilot"]
people_col = db["people"]

# In-memory session state
USER_STATE = {}

def debug(title, data):
    print("\n" + "=" * 60)
    print(f"[DEBUG] {title}")
    print("-" * 60)
    print(data)
    print("=" * 60 + "\n")
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Base URL of Node API service (Docker Compose service name)
backend_url = os.getenv(
    'backend_url',
    default="http://api:3030"   # ✅ Node service name in docker-compose.yml
)

# Sentiment analyzer microservice (if available)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)

def get_request(endpoint, **kwargs):
    url = backend_url + endpoint
    print(f"GET from {url}")
    try:
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in get_request: {e}")
        return []  # fallback empty list

def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Sentiment analysis exception occurred:", e)
        return {"sentiment": "neutral"}

def post_review(data_dict):
    request_url = f"{backend_url}/postReview"
    print(f"POST to {request_url}")
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception occurred"}

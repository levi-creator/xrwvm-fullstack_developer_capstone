# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load backend and sentiment analyzer URLs from environment variables
backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)

# -------------------------
# GET request helper
# -------------------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}"
    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception occurred"}

# -------------------------
# Sentiment analysis helper
# -------------------------
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Sentiment analysis exception occurred:", e)
        return {"error": "Sentiment analysis exception occurred"}

# -------------------------
# POST review helper
# -------------------------
def post_review(data_dict):
    request_url = f"{backend_url}/postReview"
    print("POST to {}".format(request_url))
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception occurred"}

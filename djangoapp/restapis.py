import requests
import os
import json

# ✅ Backend URL (set in .env or fallback to localhost)
backend_url = os.getenv("backend_url", "http://localhost:3030")

# -------------------------
# GET request helper
# -------------------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception"}

# -------------------------
# POST request helper
# -------------------------
def post_review(payload):
    request_url = backend_url + "/postReview"   # <-- use this
    print("POST to {}".format(request_url))
    try:
        response = requests.post(request_url, json=payload)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception"}

def post_review(data_dict):
    request_url = backend_url + "/postReview"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())  # Debugging output
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception occurred"}



# -------------------------
# Sentiment analysis helper
# -------------------------
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Network exception: {str(e)}"}
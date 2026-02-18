from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt

import logging
import json

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review, analyze_review_sentiments

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------------------
# Dealer-related views
# -------------------------

# Get dealerships (all or by state)
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Get dealer details by dealer_id
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Get dealer reviews with sentiment analysis
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# -------------------------
# Car-related views
# -------------------------
def get_local_cars(request):
    cars = CarModel.objects.select_related('car_make').all()
    data = [
        {
            "make": car.car_make.name,
            "model": car.name,
            "year": car.year,
            "type": car.type,
            "dealer_id": car.dealer_id
        }
        for car in cars
    ]
    return JsonResponse(data, safe=False)

def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})

# -------------------------
# Contact page view
# -------------------------
def contact_view(request):
    return render(request, "Contact.html")

# -------------------------
# Review submission view
# -------------------------
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Analyze sentiment before posting
        sentiment = analyze_review_sentiments(data.get("review", ""))
        data["sentiment"] = sentiment.get("sentiment", "neutral")
        result = post_review(data)
        return JsonResponse(result, safe=False)
    return JsonResponse({"error": "POST request required"}, status=400)

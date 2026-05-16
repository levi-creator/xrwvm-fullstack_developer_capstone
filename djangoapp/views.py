import logging
import json
import os

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review, analyze_review_sentiments

logger = logging.getLogger(__name__)

# -------------------------
# React entry point
# -------------------------
def index(request):
    # Serve React build index.html
    return render(request, "index.html")

# -------------------------
# Manifest.json view
# -------------------------
def manifest(request):
    path = os.path.join(settings.BASE_DIR, 'frontend/build/manifest.json')
    return FileResponse(open(path, 'rb'), content_type='application/json')

# -------------------------
# Static page views (optional legacy templates)
# -------------------------
def about(request):
    return render(request, "djangoapp/About.html")

def contact(request):
    return render(request, "Contact.html")

def home(request):
    return render(request, "djangoapp/Home.html")

# -------------------------
# Dealer-related views
# -------------------------
def get_dealerships(request, state="All"):
    try:
        if state == "All":
            endpoint = "/get_dealers"
        else:
            endpoint = f"/get_dealers?state={state}"

        dealerships = get_request(endpoint)

        if not dealerships:
            dealerships = [
                {"id": 1, "name": "Test Dealer", "state": "CA"},
                {"id": 2, "name": "Sample Motors", "state": "NY"},
                {"id": 3, "name": "Demo Cars", "state": "TX"}
            ]

        logger.info("Dealerships data: %s", dealerships)
        return JsonResponse({"status": 200, "dealers": dealerships})
    except Exception as e:
        logger.error("Error in get_dealerships: %s", e)
        return JsonResponse({"status": 500, "message": "Internal Server Error"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/get_dealer?dealerId={dealer_id}"
        dealership = get_request(endpoint) or {"id": dealer_id, "name": "Fallback Dealer"}
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/get_reviews?dealerId={dealer_id}"
        reviews = get_request(endpoint) or [{"review": "Fallback review", "sentiment": "neutral"}]
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get('review', ''))
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
# Auth views
# -------------------------
def logout(request):
    auth_logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sentiment = analyze_review_sentiments(data.get("review", ""))
        data["sentiment"] = sentiment.get("sentiment", "neutral")
        result = post_review(data)
        return JsonResponse(result, safe=False)
    return JsonResponse({"error": "POST request required"}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": user.username, "status": "success"})
            else:
                return JsonResponse({"status": "failed"}, status=401)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "invalid method"}, status=400)


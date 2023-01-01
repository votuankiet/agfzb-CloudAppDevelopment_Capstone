from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from djangoapp.apps import DjangoappConfig
from djangoapp.models import CarModel
from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
# def contact(request):
# ...
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = DjangoappConfig.get_dealership_url
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = DjangoappConfig.get_review_url
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        url = DjangoappConfig.get_dealership_url
        dealer = get_dealer_by_id_from_cf(url, dealer_id)[0]
        context["review_list"] = dealer_reviews
        context["dealer_id"] = dealer_id
        context["dealer_full_name"] = dealer.full_name
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "POST":
        user = request.user
        context = {}
        if user.id is None or not user.is_authenticated:
            context['message'] = "Please log in to submit answer."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
        car = get_object_or_404(CarModel, pk=int(request.POST["car"]))
        review = {"car_make": car.make.name,
                  "car_model": car.name,
                  "car_year": car.year.year,
                  "dealership": dealer_id,
                  "name": "{} {}".format(user.first_name, user.last_name),
                  "purchase": True if request.POST.get("purchasecheck") is not None else False,
                  "purchase_date": request.POST["purchasedate"],
                  "review": request.POST["content"],
                  }
        json_payload = {"review": review}
        url = DjangoappConfig.post_review_url
        result = post_request(url, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    elif request.method == "GET":
        context = {}
        url = DjangoappConfig.get_dealership_url
        dealer = get_dealer_by_id_from_cf(url, dealer_id)[0]
        cars = []
        car_qs = CarModel.objects.filter(dealer_id=dealer_id)
        for car in car_qs:
            cars.append(car)

        context["dealer_full_name"] = dealer.full_name
        context["dealer_id"] = dealer.id
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

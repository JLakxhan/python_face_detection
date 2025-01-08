from django.shortcuts import render, redirect
from django.contrib import messages
from user_auth.mongodb import MONGO_USER_COLLECTION
from .mongodb import MONGO_SHIFT_COLLECTION
from bson.objectid import ObjectId  # Optional, for MongoDB ID handling
from django.http import JsonResponse
import requests
import datetime
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Registration View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # # Check if user already exists
        # if MONGO_USER_COLLECTION.find_one({"email": email}):
        #     messages.error(request, "User already exists!")
        #     return redirect("register")
        
        # Insert new user into MongoDB
        # MONGO_USER_COLLECTION.insert_one({
        #     "username": username,
        #     "email": email,
        #     "password": password
        # })

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")
    return render(request, "login.html")  # Use same template for login/register

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password!")
            # return redirect('login')
        # Authenticate user
        # user = MONGO_USER_COLLECTION.find_one({"email": email, "password": password})
        # if user:
        #      # Save user ID in session
        #       # Debugging
        #     messages.success(request, "Login successful!")
        #     return redirect("home")  # Redirect to home page
        # else:
        #     print("Invalid credentials.")  # Debugging
        #     messages.error(request, "Invalid email or password!")
    return render(request, "login.html")


def home_view(request):
    return render(request, "home.html")

def dashboard_view(request):
    return render(request, "dashboard.html")



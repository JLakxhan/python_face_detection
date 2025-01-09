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
    return render(request, "login.html")


def home_view(request):
    return render(request, "home.html")

def dashboard_view(request):
    return render(request, "dashboard.html")

def userboard_view(request):
    return render(request, "user.html")

def logout_view(request):
    return render(request, "login.html")

def search_user(request):
    roleId = request.POST['role']
    if roleId != '-1':
        users = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser').filter(is_superuser=roleId)
    else:
        users = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser')

    return JsonResponse({'code': 1, 'data': list(users)})

def create(request): 
    if request.user.is_authenticated and request.user.is_superuser:
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        roleId = request.POST['role']
        email = request.POST['email']
        password = request.POST['password'] 

        usernameExist = CustomUser.objects.filter(username=username).count()
        if usernameExist == 0 :
            create_user = CustomUser(
                email=email,
                first_name=fname,
                last_name=lname,
                username=username,
                password=password,
                is_superuser=roleId
            )
            create_user.set_password(password)
            create_user.save()

            return JsonResponse({'code': 1, 'data': "User created successfully!!"})
        else:
            return JsonResponse({'code': 1, 'data': "Username already exists!!"})

def editUser(request):
    id = request.POST['id']
    email = request.POST['email']
    fname = request.POST['fname']
    lname = request.POST['lname']
    roleId = request.POST['role']

    user = CustomUser.objects.get(pk=id)
    user.email = email
    user.first_name = fname
    user.last_name = lname
    user.email = email
    user.is_superuser = roleId

    user.save()

    return JsonResponse({'code': 1,'data':"User updated successfully!!"})

def resetPasswordAdminApi(request):
    id = request.POST['id']
    password = request.POST['password']
    user = CustomUser.objects.get(pk=id)
    user.set_password(password)
    user.save()

    return JsonResponse({'code': 1,'data':"Password updated successfully!!"})
from django.shortcuts import render, redirect
from django.contrib import messages
from user_auth.mongodb import MONGO_USER_COLLECTION
from .mongodb import MONGO_SHIFT_COLLECTION
from bson.objectid import ObjectId  
from django.http import JsonResponse
import requests
import datetime
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ApplyLeave

# Registration View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")
    return render(request, "login.html")  

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
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

def logout_view(request):
    logout(request)
    return redirect('login')

def create_user_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    return render(request, "createUser.html")

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    user = request.user
    return render(request, "home.html", {'user': user})

def shift_view(request):
    return render(request, "shift.html")

def shift_history_view(request):
    return render(request, "shiftlist.html")

def userboard_view(request):
    return render(request, "users.html")

def logout_view(request):
    return render(request, "login.html")

def home_test(request):
    return render(request, "home2.html")

def apply_leave_view(request):
    if request.user.is_authenticated:
        user = request.user
        leave_balances = {
            "annual": user.leave_annual,
            "casual": user.leave_casual,
            "medical": user.leave_medical,
            "other": user.leave_other,
        }
        return render(request, "applyleave.html", {"leave_balances": leave_balances})

def leave_view(request):
    return render(request, "leave.html")

def employees_view(request):
    userslist = CustomUser.objects.order_by('id').all().values('id', 'employee_id','bio','first_name','last_name','joined_date','date_of_birth','contact_number','address','personal_email','identity_number','passport_number','emergency_contact_name','emergency_contact_number','emergency_contact_relationship','leave_annual','leave_casual','leave_medical','leave_other')
    return render(request, "employees.html", {'employees': userslist})

def leaves_view(request):
    leaves = ApplyLeave.objects.filter(user=request.user).values('id', 'leave_type', 'start_date', 'end_date', 'total_days', 'created_at')
    return render(request, "leaves.html", {'leaves': leaves})

def search_user(request):
    roleId = request.POST['role']
    if roleId != '-1':
       userslist = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser')
       userslist = list(userslist)
       users = []
       for us in userslist:
           if ((roleId == "1" and us['is_superuser'] == True) or (roleId == "0" and us['is_superuser'] == False)):
               users.append(us)
                
    else:
        users = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser')
        users = list(users)

    return JsonResponse({'code': 1, 'data': users})

def create_user(request): 
    if request.user.is_authenticated and request.user.is_superuser:
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        password = request.POST['password']
        roleId = request.POST['role']
        employee_id = request.POST['employee_id']
        joined_date = request.POST['joined_date']
        bio = request.POST['bio']
        address = request.POST['address']
        contact_number = request.POST['contact_number']
        date_of_birth = request.POST['date_of_birth']
        emergency_contact_name = request.POST['emergency_contact_name']
        emergency_contact_number = request.POST['emergency_contact_number']
        emergency_contact_relationship = request.POST['emergency_contact_relationship']
        identity_number = request.POST['identity_number']
        passport_number = request.POST['passport_number']
        personal_email = request.POST['personal_email']
        usernameExist = CustomUser.objects.filter(username=username).count()
        if usernameExist == 0 :
            create_user = CustomUser(
                username=username,
                email=email,
                first_name=fname,
                last_name=lname,
                password=password,
                is_superuser=roleId,
                employee_id=employee_id,
                joined_date=joined_date,
                bio=bio,
                address=address,
                contact_number=contact_number,
                date_of_birth=date_of_birth,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_number=emergency_contact_number,
                emergency_contact_relationship=emergency_contact_relationship,
                identity_number=identity_number,
                passport_number=passport_number,
                personal_email=personal_email
            )
            create_user.set_password(password)
            create_user.save()

            return JsonResponse({'code': 1, 'data': "User created successfully!!"})
        else:
            return JsonResponse({'code': 1, 'data': "Username already exists!!"})

#User creating leave
def create_leave(request):
    if request.user.is_authenticated:
        leave_type = request.POST.get('leave_type', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        if not start_date or not end_date:
            return JsonResponse({'code': 0, 'data': "Start date and end date are required!"})

        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Calculate the difference in days (inclusive)
        days_difference = (end_date_obj - start_date_obj).days + 1

        if days_difference < 0:
            return JsonResponse({'code': 0, 'data': "End date cannot be earlier than start date."})

        try:
            if leave_type == 'annual':
                if request.user.leave_annual < days_difference: 
                    return JsonResponse({'code': 0, 'data': "Leave balance not enough."})
                request.user.leave_annual = request.user.leave_annual - days_difference
            elif leave_type == 'casual':
                if request.user.leave_casual < days_difference: 
                    return JsonResponse({'code': 0, 'data': "Leave balance not enough."})
                request.user.leave_casual = request.user.leave_casual - days_difference
            elif leave_type == 'medical':
                if request.user.leave_medical < days_difference: 
                    return JsonResponse({'code': 0, 'data': "Leave balance not enough."})
                request.user.leave_medical = request.user.leave_medical - days_difference
            elif leave_type == 'other':
                if request.user.leave_other < days_difference: 
                    return JsonResponse({'code': 0, 'data': "Leave balance not enough."})
                request.user.leave_other = request.user.leave_other - days_difference

            leave_entry = ApplyLeave.objects.create(
                leave_type=leave_type,
                total_days=days_difference,  # Default value for total leave
                start_date=start_date,
                end_date=end_date,
                user=request.user
            )
            request.user.save()
            
            return JsonResponse({'code': 1, 'data': "Leave created successfully!", 'leave_id': leave_entry.id})
        except Exception as e:
            return JsonResponse({'code': 0, 'data': f"Error creating leave: {str(e)}"})

    return JsonResponse({'code': 0, 'data': "Unauthorized access!"})


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

# def search_user_leave(request):
#     roleId = request.POST['role']
#     if roleId != '-1':
#        userslist = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser')
#        userslist = list(userslist)
#        users = []
#        for us in userslist:
#            if ((roleId == "1" and us['is_superuser'] == True) or (roleId == "0" and us['is_superuser'] == False)):
#                users.append(us)
                
#     else:
#         users = CustomUser.objects.order_by('id').all().values('id', 'username','email','first_name','last_name','is_superuser')
#         users = list(users)

#     return JsonResponse({'code': 1, 'data': users})
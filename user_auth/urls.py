from django.urls import path
from .views import home_view, register_view, login_view,dashboard_view

urlpatterns = [ 
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path("home/", home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard")
    
]
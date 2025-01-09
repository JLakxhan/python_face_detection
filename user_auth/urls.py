from django.urls import path
from .views import home_view, register_view, login_view,dashboard_view,userboard_view,search_user,create,editUser,resetPasswordAdminApi

urlpatterns = [ 
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path("home/", home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("userboard/", userboard_view, name="dashboard")  ,
    path("user/search/", search_user, name="search_user"),
    path("user/create/", create, name="create"),
    path("user/edit/", editUser, name="editUser"),
    path("user/reset/", resetPasswordAdminApi, name="resetPasswordAdminApi"),
]
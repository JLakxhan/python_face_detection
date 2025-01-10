from django.urls import path
from .views import home_view, register_view, login_view,dashboard_view,userboard_view,search_user,editUser,resetPasswordAdminApi,logout_view,home_test,create_user

urlpatterns = [ 
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path("home/", home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("userboard/", userboard_view, name="userboard_view")  ,
    path("user/search/", search_user, name="search_user"),
    path("user/edit/", editUser, name="editUser"),
    path("user/reset/", resetPasswordAdminApi, name="resetPasswordAdminApi"),
    path("login/", logout_view, name="logout_view"),
    path("home2/", home_test, name="home_test"),
    path("users/create/", create_user, name="create_user")
]

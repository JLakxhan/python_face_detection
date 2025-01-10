from django.urls import path
from .views import home_view, register_view, login_view,dashboard_view,userboard_view,search_user,editUser,resetPasswordAdminApi,logout_view,home_test,create_user,apply_leave_view,leave_view,create_leave

urlpatterns = [ 
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path("home/", home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("userboard/", userboard_view, name="userboard_view"),
    path("login/", logout_view, name="logout_view"),
    path("home2/", home_test, name="home_test"),

    path("user/search/", search_user, name="search_user"),
    path("user/edit/", editUser, name="editUser"),
    path("user/reset/", resetPasswordAdminApi, name="resetPasswordAdminApi"),
    path("users/create/", create_user, name="create_user"),

    path("applyleave/", apply_leave_view, name="apply_leave_view"),
    path("leave/", leave_view, name="leave_view"),
    path("users/create/leave/", create_leave, name="create_leave"),
    path("user/search/leave/", search_user, name="search_user"),

]

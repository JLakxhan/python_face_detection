from django.urls import path
from .views import home_view, login_view,userboard_view,search_user,editUser,resetPasswordAdminApi,logout_view,home_test,create_user,apply_leave_view,leave_view,create_leave, shift_view, shift_history_view, create_user_view,employees_view,logout_view, leaves_view, edit_user_view, edit_user

urlpatterns = [ 
    path("shift-history/", shift_history_view, name="shift_history"),
    path("shift/", shift_view, name="shift"),
    path("home/", home_view, name="home"),
    path("userboard/", userboard_view, name="userboard_view"),
    path("create-user/", create_user_view, name="create_user"),
    path("edit-user/", edit_user_view, name="edit_user"),
    path("employees/", employees_view, name="employee"),
    path("leaves/", leaves_view, name="leaves"),
    path("logout/", logout_view, name="logout"),
    path('', login_view, name='login'),
    
    path("home2/", home_test, name="home_test"),

    path("user/search/", search_user, name="search_user"),
    path("user/edit/", editUser, name="editUser"),
    path("user/reset/", resetPasswordAdminApi, name="resetPasswordAdminApi"),
    path("users/create/", create_user, name="create_user"),
    path("users/edit/", edit_user, name="edit_user"),

    path("applyleave/", apply_leave_view, name="apply_leave_view"),
    path("leave/", leaves_view, name="leaves_view"),
    path("users/create/leave/", create_leave, name="create_leave"),
    path("user/search/leave/", search_user, name="search_user"),

]

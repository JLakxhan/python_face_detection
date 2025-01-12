from django.urls import path
from .views import analyze_emotion_and_stress,start_shift,end_shift,shift_status,analyze_avg_emotion,analyze_notification,search_shift,prediction_view

urlpatterns = [ 
    path("analyze/", analyze_emotion_and_stress, name="analyze_emotion_and_stress"),
    path("shift/start/", start_shift, name="start_shift"),
    path("shift/end/", end_shift, name="end_shift"),
    path("shift/status/", shift_status, name="shift_status"),
    path("shift/avg/", analyze_avg_emotion, name="analyze_avg_emotion"),
    path("shift/notification/", analyze_notification, name="analyze_notification"),
    path("shift/search/", search_shift, name="search_shift"),
    path("prediction/", prediction_view, name="prediction_view"),

]
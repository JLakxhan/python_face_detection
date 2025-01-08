from django.urls import path
from .views import analyze_emotion_and_stress,start_shift,end_shift

urlpatterns = [ 
    path("analyze/", analyze_emotion_and_stress, name="analyze_emotion_and_stress"),
    path("shift/start/", start_shift, name="start_shift"),
    path("shift/end/", end_shift, name="end_shift")
]
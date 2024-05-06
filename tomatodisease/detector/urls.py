from django.urls import path, include
from detector.views import TomatoDetector

urlpatterns = [
    path('', TomatoDetector.as_view()),
]

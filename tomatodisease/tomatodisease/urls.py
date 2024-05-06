from django.contrib import admin
from django.urls import path, include
from detector import urls as detector_urls
from . import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(detector_urls)),
]

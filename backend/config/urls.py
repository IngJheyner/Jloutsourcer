"""
URL configuration for Cooperative Backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API REST
    path('api/', include('app_affiliate.api.urls')),
]

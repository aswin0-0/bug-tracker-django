from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bugged.urls')),  # 🔗 This includes both frontend and API routes
]

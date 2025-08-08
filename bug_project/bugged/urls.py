from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 🧩 HTML Views
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('bugs/', bugs, name='bugs'),
    path('profile/', profile, name='profile'),
    path('bugs/update/<int:bug_id>/', update_bug_status, name='update_bug'),

    # 🧩 API Views
    path('api/register/', api_register),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/bugs/', api_bugs),
    path('api/bugs/add/', api_add_bug),
]
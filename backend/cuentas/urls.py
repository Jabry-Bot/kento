from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("google/", views.login_google, name="login_google"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("yo/", views.yo, name="yo"),
]

from django.urls import path
from bot import views

urlpatterns = [
    path("verify", views.BotVerificationView.as_view(), name="verify"),
]
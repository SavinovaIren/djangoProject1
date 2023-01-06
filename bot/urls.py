from django.urls import path
from bot import views

urlpatterns = [
    path("verify", views.BotVerifyView.as_view(), name="verify"),
]
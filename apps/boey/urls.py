from django.urls import path

from . import views

app_name = "boey"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]

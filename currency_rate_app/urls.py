from django.urls import path

from . import views

urlpatterns = [
    path("load_data/", views.LoadDataView.as_view(), name="load_data"),
    path("get_rate/", views.GetRateView.as_view(), name="get_rate"),
]

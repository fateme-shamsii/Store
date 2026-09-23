from django.urls import path
from advertisment import views

urlpatterns = [
    path('', views.AdvertisementListCreateView.as_view(), name='advertisment')
]
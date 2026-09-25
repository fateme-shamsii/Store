from django.urls import path
from advertisment import views

urlpatterns = [
    path('advertisment/', views.AdvertisementListCreateView.as_view(), name='advertisment')
]
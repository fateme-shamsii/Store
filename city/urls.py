from django.urls import path
from city import views

urlpatterns = [
    path('', views.ListCityView.as_view(), name='city'),

]
from django.urls import path
from brand import views

urlpatterns = [
    path('', views.BrandListView.as_view(), name='brand')
]
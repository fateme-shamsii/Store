from django.urls import path
from store import views

urlpatterns = [
    path('', views.StoreListCreateView.as_view(), name='store-list-create'),
]
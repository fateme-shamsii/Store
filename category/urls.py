from django.urls import path
from category import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
]
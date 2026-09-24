from django.urls import path
from orders import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='orders_list'),
]
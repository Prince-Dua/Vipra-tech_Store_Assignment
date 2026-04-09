from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='index'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.SuccessView.as_view(), name='success'),
]
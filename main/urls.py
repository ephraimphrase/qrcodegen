from django.urls import path
from . import views

urlpatterns = [
    path('qrCodeGen', views.qrCodeGen, name="qrCodeGen"),
    path('home/', views.home, name='home'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn/', views.signIn, name='signIn'),
    path('signOut/', views.signOut, name='signOut'),
    path('', views.landing, name='landing'),
    path('productInfo/<str:pk>/', views.productInfo, name='productInfo'),
    path('scanner/', views.scanner, name='scanner'),
]

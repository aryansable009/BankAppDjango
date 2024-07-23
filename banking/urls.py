from django.urls import path
from django.urls import re_path as url
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_view, name='register'),
    path('accounts/', views.accounts,  name='accounts'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('submit_transfer/', views.submit_transfer, name='submit_transfer'),
    path('submit_withdraw/', views.submit_withdraw, name='submit_withdraw'),
    path('submit_deposit/', views.submit_deposit, name='submit_deposit'),
]
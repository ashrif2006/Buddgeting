from django.urls import path 
from . import views

urlpatterns = [
    path('' ,views.home , name = 'home'),
    path('transactions/', views.transactions, name='transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('goals/', views.goals, name='goals'),
    path('budgets/', views.budgets, name='budgets'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]

from django.urls import path
from . import views 

urlpatterns = [
    path('add/', views.AddBank.as_view(), name='add_bank'),
    path('<int:bank_id>/add_branch/', views.AddBranch.as_view(), name='add_branch'),
    path('', views.AllBanks.as_view(), name='bank_list'),
    path('<int:bank_id>/details/', views.BankIdDetails.as_view(), name='bank_details'),
    path('branch/<int:branch_id>/details/', views.BranchIdDetails.as_view(), name='branch_details'),
    path('branch/<int:branch_id>/edit/', views.EditBranch.as_view(), name='edit_branch'),
]

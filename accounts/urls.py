from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/view/', views.ProfileView.as_view(), name='profile_view'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
]

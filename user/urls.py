from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in_user, name='sign_in_user'),
    path('sign-out/', views.sign_out_user, name='sign_out_user'),
    path('sign-up/', views.sign_up_user, name='sign_up_user'),
    path('about-realtor/<int:id>/', views.about_realtor, name='about_realtor'),
    path('profile/', views.profile_realtor, name='profile_realtor'),
    path('profile-renter/', views.profile_renter, name='profile_renter'),
    path('update-profile-realtor/', views.update_profile_realtor, name='update_profile_realtor'),
    path('update-profile-renter/', views.update_profile_renter, name='update_profile_renter'),
]
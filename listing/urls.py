from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_listing_view, name='manage_listing'),
    path('detail/<int:id>/', views.detail_listing_view, name='detail_listing'),
    path('get-listings/', views.listings_view, name='get_listings'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property, name='edit_property'),
    path('delete-property/<int:id>/', views.delete_property, name='delete_property'),
    path('review-listing/', views.review_listing, name='review_listing'),
]
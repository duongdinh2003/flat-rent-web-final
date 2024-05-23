from django.contrib import admin
from .models import Listing, Purchasing, ListingReview

# Register your models here.
admin.site.register(Listing)

admin.site.register(Purchasing)

admin.site.register(ListingReview)
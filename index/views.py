from django.shortcuts import render
from listing.models import Listing

# Create your views here.
def home(request):
    listings_latest = Listing.objects.filter(is_published=True).order_by('-date_created')[:3]
    listings = Listing.objects.filter(is_published=True)[:6]
    context = {
        'listings_latest': listings_latest,
        'listings': listings
    }
    return render(request, 'index.html', context)

def search_nearby(request):
    return render(request, 'search_nearby.html')
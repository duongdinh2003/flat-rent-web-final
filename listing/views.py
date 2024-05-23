from django.shortcuts import render, redirect
from .models import Listing, ListingReview
from user.models import UserAccount, UserInformation
from datetime import datetime
from django.core.paginator import Paginator
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def manage_listing_view(request):
    user = request.user

    if not user.is_realtor:
        return redirect('index')
    else:
        listings = Listing.objects.filter(realtor=user.email).order_by('id')

        pagi = Paginator(listings, 3)
        page_number = request.GET.get('page')
        page_obj = pagi.get_page(page_number)
        nums = page_obj.paginator.num_pages
        num_page = [i for i in range(1, nums+1)]

        context = {
            'page_obj': page_obj,
            'num_page': num_page
        }

        return render(request, 'manage_listings.html', context)
    
def detail_listing_view(request, id):
    listing = Listing.objects.get(id=id)
    realtor = UserAccount.objects.get(email=listing.realtor)
    realtor_info = UserInformation.objects.get(user_id=realtor.id)
    recent_listings = Listing.objects.filter(is_published=True)[:5]
    context = {
        'listing': listing,
        'realtor': realtor,
        'realtor_info': realtor_info,
        'recent_listings': recent_listings
    }
    return render(request, 'detail.html', context)

def listings_view(request):
    listings = Listing.objects.all()
    context = {
        'listings': listings
    }
    return render(request, 'listings.html', context)

@login_required
def add_property(request):
    if request.method == 'POST':
        realtor = request.user.email
        title = request.POST['title']
        slug = title.lower().replace(' ', '-')
        address = request.POST['address']
        city = request.POST['city']
        description = request.POST['description']
        price = request.POST['price']
        bedrooms = request.POST['bedrooms']
        bathrooms = request.POST['bathrooms']
        sale_type = request.POST['sale_type']
        home_type = request.POST['home_type']
        main_photo = request.FILES.get('main_photo', None)
        photo_1 = request.FILES.get('photo_1', None)
        photo_2 = request.FILES.get('photo_2', None)
        photo_3 = request.FILES.get('photo_3', None)
        published = False
        date_created = request.POST['date_created']
        date_created_obj = datetime.strptime(date_created, '%m/%d/%Y')
        date_created_obj = make_aware(date_created_obj)
        area = request.POST['area']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        listing = Listing(
            realtor=realtor,
            title=title,
            slug=slug,
            address=address,
            city=city,
            description=description,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            sale_type=sale_type,
            home_type=home_type,
            main_photo=main_photo,
            photo_1=photo_1,
            photo_2=photo_2,
            photo_3=photo_3,
            is_published=published,
            date_created=date_created_obj,
            area=area,
            latitude=latitude,
            longitude=longitude
        )
        listing.save()
        messages.success(request, 'Add property successfully!')
        return redirect('manage_listing')
    else:
        home_type_list = Listing.HomeType.values
        sale_type_list = Listing.SaleType.values

        context = {
            'home_type_list': home_type_list,
            'sale_type_list': sale_type_list
        }
        return render(request, 'add_property.html', context)

@login_required
def edit_property(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        slug = title.lower().replace(' ', '-')
        address = request.POST['address']
        city = request.POST['city']
        description = request.POST['description']
        price = request.POST['price']
        bedrooms = request.POST['bedrooms']
        bathrooms = request.POST['bathrooms']
        sale_type = request.POST['sale_type']
        home_type = request.POST['home_type']
        main_photo = request.FILES.get('main_photo', None)
        photo_1 = request.FILES.get('photo_1', None)
        photo_2 = request.FILES.get('photo_2', None)
        photo_3 = request.FILES.get('photo_3', None)
        published = request.POST.get('published') == 'on'
        date_created = request.POST['date_created']
        date_created_obj = datetime.strptime(date_created, '%m/%d/%Y')
        date_created_obj = make_aware(date_created_obj)
        area = request.POST['area']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        listing.title = title
        listing.slug = slug
        listing.address = address
        listing.city = city
        listing.description = description
        listing.price = price
        listing.bedrooms = bedrooms
        listing.bathrooms = bathrooms
        listing.sale_type = sale_type
        listing.home_type = home_type

        if main_photo:
            listing.main_photo = main_photo
        if photo_1:
            listing.photo_1 = photo_1
        if photo_2:
            listing.photo_2 = photo_2
        if photo_3:
            listing.photo_3 = photo_3
        
        listing.is_published = published
        listing.date_created = date_created_obj
        listing.area = area
        listing.latitude = latitude
        listing.longitude = longitude

        listing.save()
        messages.success(request, 'Edit property successfully!')
        return redirect('manage_listing')
    else:
        home_type_list = Listing.HomeType.values
        sale_type_list = Listing.SaleType.values
        date_cre = listing.date_created.strftime('%m/%d/%Y')

        context = {
            'listing': listing,
            'home_type_list': home_type_list,
            'sale_type_list': sale_type_list,
            'date_cre': date_cre
        }

        return render(request, 'edit_property.html', context)

@login_required
def delete_property(request, id):
    listing = Listing.objects.get(id=id)
    listing.delete()
    messages.info(request, 'Delete property successfully!')
    return redirect('manage_listing')

def review_listing(request):
    if request.method == 'POST':
        user = request.user
        review = request.POST['review']
        vote = request.POST['vote']
        listing_id = request.POST['id_property']
        listing = Listing.objects.get(id=listing_id)

        listing_review = ListingReview(
            customer=user.email,
            review=review,
            vote=vote,
            listing=listing
        )

        listing_review.save()
        messages.info(request, 'Thank you so much for reviewing this property!')
        return redirect('index')
    
    return redirect('detail_listing')

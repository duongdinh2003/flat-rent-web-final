from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserAccount, UserInformation
from listing.models import Listing
from .helpers import get_reviews_of_realtor

# Create your views here.
def profile_realtor(request):
    realtor = request.user
    realtor_info = UserInformation.objects.get(user_id=realtor.id)
    listing_reviews = get_reviews_of_realtor(realtor)
    
    context = {
        'realtor': realtor,
        'realtor_info': realtor_info,
        'listing_reviews': listing_reviews
    }
    return render(request, 'profile.html', context)

def profile_renter(request):
    renter = request.user
    renter_info = UserInformation.objects.get(user_id=renter.id)
    context = {
        'renter': renter,
        'renter_info': renter_info
    }
    return render(request, 'profile_renter.html', context)

def sign_in_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'You signed in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Incorrect email or password')
            return redirect('index')
    
    context = {
        'sign_in': True
    }
    return render(request, 'index.html', context)

def sign_out_user(request):
    logout(request)
    messages.info(request, 'You were signed out')
    return redirect('index')

def sign_up_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        user_type = request.POST['user_type']

        if user_type == 'realtor':
            user = UserAccount.objects.create_realtor(email=email, name=name, password=password)
        else:
            user = UserAccount.objects.create_user(email=email, name=name, password=password)
        
        user_info = UserInformation(
            user=user
        )
        user_info.save()

        login(request, user)
        messages.success(request, 'You signed up successfully!')
        return redirect('index')

def about_realtor(request, id):
    realtor = UserAccount.objects.get(id=id)
    realtor_info = UserInformation.objects.get(user_id=realtor.id)
    properties = Listing.objects.filter(realtor=realtor.email)
    listing_reviews = get_reviews_of_realtor(realtor)
    context = {
        'realtor': realtor,
        'realtor_info': realtor_info,
        'properties': properties,
        'listing_reviews': listing_reviews
    }
    return render(request, 'about_realtor.html', context)

def update_profile_realtor(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar_agent', None)
        name = request.POST['name_agent']
        experience = request.POST['experience_agent']
        company = request.POST['company_agent']
        address = request.POST['address_agent']
        phone_number = request.POST['phone_number_agent']
        bio = request.POST['bio_agent']

        realtor = request.user
        realtor_info = UserInformation.objects.get(user_id=realtor.id)
        
        realtor.name = name
        realtor_info.experience = experience
        realtor_info.company = company
        realtor_info.address = address
        realtor_info.phone_number = phone_number
        realtor_info.bio = bio

        if avatar:
            realtor_info.avatar = avatar
        
        realtor.save()
        realtor_info.save()

        messages.info(request, 'Updated profile successfully!')
        return redirect('profile_realtor')
    
    return redirect('profile_realtor')

def update_profile_renter(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar_renter', None)
        name = request.POST['name_renter']
        address = request.POST['address_renter']
        phone_number = request.POST['phone_number_renter']
        bio = request.POST['bio_renter']

        renter = request.user
        renter_info = UserInformation.objects.get(user_id=renter.id)

        renter.name = name
        renter_info.address = address
        renter_info.phone_number = phone_number
        renter_info.bio = bio

        if avatar:
            renter_info.avatar = avatar
        
        renter.save()
        renter_info.save()

        messages.info(request, 'Updated profile successfully!')
        return redirect('profile_renter')
    
    return redirect('profile_renter')

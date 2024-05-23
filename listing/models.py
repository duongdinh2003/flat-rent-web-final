from django.db import models
from django.utils.timezone import now

# Create your models here.
class Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        TOWNHOUSE = 'Townhouse'
        APARTMENT = 'Apartment'
        RESORT = 'Resort'
        VILLA = 'Villa'
    
    realtor = models.EmailField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    price = models.BigIntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sale_type = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=10, choices=HomeType.choices, default=HomeType.HOUSE)
    main_photo = models.ImageField(upload_to='listings/')
    photo_1 = models.ImageField(upload_to='listings/')
    photo_2 = models.ImageField(upload_to='listings/')
    photo_3 = models.ImageField(upload_to='listings/')
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    area = models.IntegerField(null=True, blank=True)
    is_inbusiness = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

class Purchasing(models.Model):
    customer = models.EmailField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    months = models.SmallIntegerField(null=True, blank=True)

class ListingReview(models.Model):
    class Vote(models.IntegerChoices):
        AWFUL = 1
        BAD = 2
        MEDIUM = 3
        GOOD = 4
        GREAT = 5

    customer = models.EmailField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    vote = models.IntegerField(choices=Vote.choices, default=Vote.MEDIUM)

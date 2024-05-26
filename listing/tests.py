from django.test import TestCase, Client
from django.urls import reverse
from .models import Listing, ListingReview
from user.models import UserAccount, UserInformation
from django.utils.timezone import make_aware
from datetime import datetime

# Create your tests here.
class ListingTestCase(TestCase):
    databases = { 'users', 'listings' }

    def setUp(self):
        self.client = Client()
        self.user = UserAccount.objects.create_realtor(
            email='testuser@example.com',
            name='Test User',
            password='password123',
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.user_info = UserInformation.objects.create(
            user=self.user,
            address='123 Test Street',
            phone_number='0123456789',
            bio='Test Bio'
        )
        self.listing = Listing.objects.create(
            realtor=self.user.email,
            title='Test Listing',
            slug='test-listing',
            address='123 Test Street',
            city='Sample City',
            description='Test description',
            price=2000,
            bedrooms=5,
            bathrooms=3,
            sale_type=Listing.SaleType.FOR_SALE,
            home_type=Listing.HomeType.HOUSE,
            main_photo='listings/example.jpg',
            photo_1='listings/example1.jpg',
            photo_2='listings/example2.jpg',
            photo_3='listings/example3.jpg',
            is_published=False,
            date_created=make_aware(datetime.now()),
            area=100,
            latitude=0.0,
            longitude=0.0
        )
    
    def test_manage_listing_view(self):
        response = self.client.get(reverse('manage_listing'))
        self.assertEqual(self.user_info.user.is_realtor, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_listings.html')
        self.assertContains(response, 'Test Listing')

    def test_detail_listing_view(self):
        response = self.client.get(reverse('detail_listing', args=[self.listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Listing')
        self.assertContains(response, '123 Test Street')
        self.assertContains(response, 'Test description')
        self.assertContains(response, 2000)
        self.assertContains(response, 5)
        self.assertContains(response, 3)
        self.assertContains(response, 'listings/example.jpg')
        self.assertTemplateUsed(response, 'detail.html')

    def test_add_property(self):
        response = self.client.post(reverse('add_property'), {
            'realtor': self.user_info.user.email,
            'title': 'New Listing',
            'slug': 'new-listing',
            'address': '456 New Street',
            'city': 'New City',
            'description': 'New description',
            'price': 3000,
            'bedrooms': 2,
            'bathrooms': 2,
            'sale_type': Listing.SaleType.FOR_SALE,
            'home_type': Listing.HomeType.CONDO,
            'main_photo': 'listings/new_photo.jpg',
            'photo_1': 'listings/new_photo1.jpg',
            'photo_2': 'listings/new_photo2.jpg',
            'photo_3': 'listings/new_photo3.jpg',
            'date_created': '05/10/2024',
            'area': 200,
            'latitude': 15.898795,
            'longitude': 108.540428
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Listing.objects.filter(slug='new-listing').exists())
        
    def test_edit_property(self):
        response = self.client.post(reverse('edit_property', args=[self.listing.id]), {
            'title': 'Update Listing',
            'slug': 'update-listing',
            'address': '456 Update Street',
            'city': 'Update City',
            'description': 'Update description',
            'price': 3500,
            'bedrooms': 3,
            'bathrooms': 3,
            'sale_type': 'For Rent',
            'home_type': 'Villa',
            'main_photo': 'listings/update_photo.jpg',
            'photo_1': 'listings/update_photo1.jpg',
            'photo_2': 'listings/update_photo2.jpg',
            'photo_3': 'listings/update_photo3.jpg',
            'date_created': '05/15/2024',
            'area': 250,
            'latitude': 16.898795,
            'longitude': 107.540428
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, 'Update Listing')
        self.assertEqual(self.listing.slug, 'update-listing')
        self.assertEqual(self.listing.address, '456 Update Street')
        self.assertEqual(self.listing.city, 'Update City')
        self.assertEqual(self.listing.description, 'Update description')
        self.assertEqual(self.listing.price, 3500)
        self.assertEqual(self.listing.bedrooms, 3)
        self.assertEqual(self.listing.bathrooms, 3)
        self.assertEqual(self.listing.sale_type, 'For Rent')
        self.assertEqual(self.listing.home_type, 'Villa')
        # self.assertEqual(self.listing.main_photo, 'listings/update_photo.jpg')
        # self.assertEqual(self.listing.photo_1, 'listings/update_photo1.jpg')
        # self.assertEqual(self.listing.photo_2, 'listings/update_photo2.jpg')
        # self.assertEqual(self.listing.photo_3, 'listings/update_photo3.jpg')
        date_created_obj = datetime.strptime('05/15/2024', '%m/%d/%Y')
        date_created_obj = make_aware(date_created_obj)
        self.assertEqual(self.listing.date_created, date_created_obj)
        self.assertEqual(self.listing.area, 250)
        self.assertEqual(self.listing.latitude, 16.898795)
        self.assertEqual(self.listing.longitude, 107.540428)

    def test_delete_property(self):
        response = self.client.post(reverse('delete_property', args=[self.listing.id]))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Listing.objects.filter(slug='test-listing').exists())
    
    def test_review_listing(self):
        response = self.client.post(reverse('review_listing'), {
            'customer': self.user_info.user.email,
            'review': 'Test Review',
            'vote': 5,
            'id_property': self.listing.id,
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ListingReview.objects.filter(review='Test Review').exists())

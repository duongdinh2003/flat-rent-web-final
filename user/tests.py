from django.test import TestCase, Client
from django.urls import reverse
from .models import UserAccount, UserInformation

# Create your tests here.
class UserAccountTestCase(TestCase):
    databases = { 'users', 'listings' }

    def setUp(self):
        self.client = Client()
        self.user = UserAccount.objects.create_realtor(
            email='testuser@example.com',
            name='Test User',
            password='password123',
        )
        self.user_info = UserInformation.objects.create(
            user=self.user,
            address='123 Test Street',
            phone_number='0123456789',
            bio='Test Bio'
        )

    def test_sign_in_user(self):
        response = self.client.post(reverse('sign_in_user'), {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_sign_out_user(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('sign_out_user'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_sign_up_user(self):
        response = self.client.post(reverse('sign_up_user'), {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123',
            'user_type': 'realtor'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserAccount.objects.filter(email='newuser@example.com').exists())

    def test_about_realtor(self):
        response = self.client.get(reverse('about_realtor', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Test Bio')

    def test_profile_realtor(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('profile_realtor'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, '123 Test Street')

    def test_profile_renter(self):
        self.user.is_realtor = False
        self.user.save()
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('profile_renter'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, '123 Test Street')
    
    def test_update_profile_realtor(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(reverse('update_profile_realtor'), {
            'name_agent': 'Updated Name',
            'experience_agent': 4,
            'company_agent': 'Company ABC',
            'address_agent': '456 New Address',
            'phone_number_agent': '0987654321',
            'bio_agent': 'Updated Bio'
        })
        self.assertEqual(response.status_code, 302)
        self.user_info.refresh_from_db()
        self.assertEqual(self.user_info.user.name, 'Updated Name')
        self.assertEqual(self.user_info.experience, 4)
        self.assertEqual(self.user_info.company, 'Company ABC')
        self.assertEqual(self.user_info.address, '456 New Address')
        self.assertEqual(self.user_info.phone_number, '0987654321')
        self.assertEqual(self.user_info.bio, 'Updated Bio')

    def test_update_profile_renter(self):
        self.user.is_realtor = False
        self.user.save()
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(reverse('update_profile_renter'), {
            'name_renter': 'Updated Name',
            'address_renter': '789 Another Address',
            'phone_number_renter': '0987654123',
            'bio_renter': 'Another Bio'
        })
        self.assertEqual(response.status_code, 302)
        self.user_info.refresh_from_db()
        self.assertEqual(self.user_info.user.name, 'Updated Name')
        self.assertEqual(self.user_info.address, '789 Another Address')
        self.assertEqual(self.user_info.phone_number, '0987654123')
        self.assertEqual(self.user_info.bio, 'Another Bio')

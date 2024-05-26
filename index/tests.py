from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class IndexTestCase(TestCase):
    databases = { 'listings' }

    def setUp(self):
        self.client = Client()
    
    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

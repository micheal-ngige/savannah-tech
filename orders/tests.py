from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from customers.models import Customer
from orders.models import Order
from django.contrib.auth.models import User

class OrderTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name="Test Customer", code="CUST123", phone="123456789")
        self.client = APIClient()
        self.client.login(username='testuser', password='12345')

    def test_create_order(self):
        data = {
            'customer': self.customer.id,
            'item': 'Test Item',
            'amount': '99.99'
        }
        response = self.client.post(reverse('order-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

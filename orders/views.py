from django.conf import settings
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
import africastalking  # Import the Africa's Talking SDK

# Initialize the Africa's Talking SDK
username = settings.AFRICAS_TALKING_USERNAME  # Use 'sandbox' for testing
api_key = settings.AFRICAS_TALKING_API_KEY
africastalking.initialize(username, api_key)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user.customer)
        self.send_sms(order.customer.phone, order.item, order.amount)

    def send_sms(self, phone, item, amount):
        message = f"Thank you for your order of '{item}' amounting to ${amount}. We appreciate your business!"
        try:
            response = africastalking.SMS.send(message, [phone])
            print("SMS sent successfully:", response)
        except Exception as e:
            print("Error sending SMS:", e)

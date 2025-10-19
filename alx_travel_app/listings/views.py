from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ListingSerializer, BookingSerializer
from .models import Listing, Booking
from rest_framework import viewsets
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import Payment
# Create your views here.
@api_view(['GET'])
def test_api(request):
    return Response({"message": "ALX Travel App API is working!"})

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def initiate_payment(request):
    booking_reference = request.GET.get('booking_reference')
    amount = request.GET.get('amount')
    callback_url = request.build_absolute_uri('/verify-payment/')

    data = {
        "amount": amount,
        "currency": "ETB",
        "email": "dizookevin@gmail.com",  
        "tx_ref": booking_reference,
        "callback_url": callback_url,
        "first_name": "John",
        "last_name": "Doe"
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=data, headers=headers)
    res_json = response.json()

    if res_json.get("status") == "success":
        Payment.objects.create(booking_reference=booking_reference, amount=amount, transaction_id=res_json['data']['id'])
        return JsonResponse({"checkout_url": res_json['data']['checkout_url']})
    return JsonResponse({"error": res_json.get("message")}, status=400)

def verify_payment(request, tx_id):
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{tx_id}", headers=headers)
    res_json = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_id)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)

    status = res_json['data']['status']
    payment.status = status.capitalize()
    payment.save()

    if status == 'success':
        # Trigger Celery task to send confirmation email
        # send_confirmation_email.delay(payment.booking_reference)
        pass

    return JsonResponse({"status": payment.status})

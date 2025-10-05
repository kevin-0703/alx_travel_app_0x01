from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ListingSerializer, BookingSerializer
from .models import Listing, Booking
from rest_framework import viewsets
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
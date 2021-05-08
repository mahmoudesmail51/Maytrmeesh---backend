from django.shortcuts import render

from core.models import *
from core.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegestirationSerializer

    def create(self, request, *args, **kwargs):
        """ post request"""
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            customer = serializer.save()
            data['response'] = "Customer registered successfully"
            data['email'] = customer.user.email
            data['first_name'] = customer.first_name
            token = Token.objects.get(user=customer.user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
    
    def list(self, request, *args, **kwargs):
        name = self.request.query_params.get('item_ids')
        return Response(name)
    





class FoodVenueViewSet(viewsets.ModelViewSet):
    queryset = FoodVenue.objects.all()
    serializer_class = FoodVenueSerializer

    def create(self, request, *args , **kwargs):
        serializer = self.get_serializer(data = request.data)
        data = {}
        if serializer.is_valid():
            venue = serializer.save()
            data['response'] = "Saved successfully"
            data['name'] = venue.name
        else:
            data = serializer.errors
        
        return Response(data)

    def list(self, request, *args, **kwargs):
        if request.data:
            location = request.data['location']
            filtered_venues = self.queryset.filter(location = location)
        else:
            filtered_venues = self.queryset
        serializer = self.get_serializer(filtered_venues, many= True)
        if serializer.data:
            return Response(serializer.data)
        return Response("No available venues")

    def update(self, request, *args, **kwargs):

        venue = self.get_object()
        data = request.data
        owner = User.objects.get_user(id= data['owner'])
        if owner:
            venue.owner = owner
            venue.name = data['name']
            venue.location = data['location']
            venue.image = data['image']
            venue.bank_account_number = data['bank_account_number']
            venue.save()
            serializer = self.get_serializer(venue)
            return Response(serializer.data)
        else:
            return Response("owner not found",status = 404)
        
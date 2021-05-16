from django.shortcuts import render

from core.models import *
from core.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view

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
    
    
    
    @action(methods=['post'], detail=True)
    def hi(self, request,**kwargs):
        customer = Customer.objects.get(user = request.user.id)
        return Response(customer.id)


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
    

    @action(detail=True)
    def getItems(self,request,**kwargs):
        food_venue = self.get_object()
        items = Item.objects.filter(food_venues=food_venue)
        serializer = ItemSerializer(items, many = True)
        if serializer.data:
            return Response(serializer.data)      
        return Response("No items available for this food venue", status = 404)

    
    @action(detail=True,methods=['POST','GET'])
    def review(self,request,**kwargs):
        if request.method == 'GET':
            """ get all reviews for a specific food venue"""
            food_venue = self.get_object()
            reviews = Review.objects.filter(food_venue= food_venue )
            serializer = ReviewSerializer(reviews, many= True)
            if serializer.data:
                return Response(serializer.data)
            return Response("No reviews available for this food venue",status = 404)
        else:
            """ Post request , add review for a specific food venue for a specific customer"""
            data = {}
            data['comment']= request.data['comment']
            data['rating']= request.data['rating']
            data['customer']= request.data['customer_id']
            data['food_venue']= kwargs['pk']
            serializer = ReviewSerializer(data= data)
            temp = {}
            if serializer.is_valid():
                review = serializer.save()
                temp['response'] = "Review added"
                temp ['comment'] = review.comment
            else:
                temp = serializer.errors
            return Response(temp)

        
    
   


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=True,methods=['POST'])
    def favorite(self, request, **kwargs):
        """ get customer """
        item = self.get_object()
        customer = Customer.objects.get(user= request.user.id)
        if not (favorite_item.objects.check_if_liked(customer,item)):
            favorite_item.objects.add(customer,item)
            return Response("Favorite")
        return Response("Already favorite")

    
    @action(detail = True,methods)
    





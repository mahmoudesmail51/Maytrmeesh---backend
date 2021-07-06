from django.db.models import query
from django.shortcuts import render

from core.models import *
from core.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework import filters


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
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many= True)
        return Response(serializer.data)

  
    
    
    @action(methods=['post'], detail=True)
    def hi(self, request,**kwargs):
        customer = Customer.objects.get(user = request.user.id)
        return Response(customer.id)




class FoodVenueViewSet(viewsets.ModelViewSet):
    queryset = FoodVenue.objects.all()
    serializer_class = FoodVenueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']



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
    

    @action(detail=True,url_path='Items')
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
        item.favorite_by.add(customer)
        item.save()
        return Response("Success")
        

      


    @action(detail=True, methods=['POST'],url_path='assign')
    def assign_foodvenue(self,request, **kwargs):
        item = self.get_object()
        food_venue_id = request.data['food_venue']
        exist = FoodVenue.objects.is_exist(food_venue_id)
        if exist:
            food_venue = FoodVenue.objects.get(id=food_venue_id)
            item.food_venues.add(food_venue)
            return Response("Assigned Successfully")
        else:
            return Response("Food venue not found")

        
        
       
    

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    
    @action(detail=True,methods=['POST'])
    def favorite(self, request, **kwargs):
        """ get customer """
        package = self.get_object()
        customer = Customer.objects.get(user= request.user.id)
        package.favorite_by.add(customer)
        package.save()
        return Response("Success")
        
    




class AvailableItemsViewSet(viewsets.ModelViewSet):
    queryset = available_item.objects.all()
    serializer_class = AvailableItemsSerialzier

    def create(self, request, *args , **kwargs):
        """ adds a new item"""
        serializer = self.get_serializer(data = request.data)
        data = {}
        if serializer.is_valid():
            available_item = serializer.save()
            data['response'] = "Added successfully"
            data['item_name'] = available_item.item.name
        else:
            data = serializer.errors
        return Response(data)